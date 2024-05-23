/* SPDX-FileCopyrightText: 2021 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

/** \file
 * \ingroup draw
 */

#include "MEM_guardedalloc.h"

#include "BKE_mesh.hh"

#include "BLI_math_vector_types.hh"

#include "extract_mesh.hh"

#include "draw_subdivision.hh"

namespace blender::draw {

/* ---------------------------------------------------------------------- */
/** \name Extract Edit UV angle stretch
 * \{ */

struct UVStretchAngle {
  /* NOTE: To more easily satisfy cross-platform alignment requirements, placing the 4-byte aligned
   * 2 element array first ensures each attribute block is 4-byte aligned. */
  int16_t uv_angles[2];
  int16_t angle;
#if defined(WITH_METAL_BACKEND)
  /* For apple platforms, vertex data struct must align to minimum per-vertex-stride of 4 bytes.
   * Hence, this struct needs to align to 8 bytes. */
  int16_t _pad0;
#endif
};
#if defined(WITH_METAL_BACKEND)
BLI_STATIC_ASSERT_ALIGN(UVStretchAngle, 4)
#endif

struct MeshExtract_StretchAngle_Data {
  UVStretchAngle *vbo_data;
  const float2 *uv;
  float auv[2][2], last_auv[2];
  float av[2][3], last_av[3];
  int cd_ofs;
};

static void compute_normalize_edge_vectors(float auv[2][2],
                                           float av[2][3],
                                           const float uv[2],
                                           const float uv_prev[2],
                                           const float co[3],
                                           const float co_prev[3])
{
  /* Move previous edge. */
  copy_v2_v2(auv[0], auv[1]);
  copy_v3_v3(av[0], av[1]);
  /* 2d edge */
  sub_v2_v2v2(auv[1], uv_prev, uv);
  normalize_v2(auv[1]);
  /* 3d edge */
  sub_v3_v3v3(av[1], co_prev, co);
  normalize_v3(av[1]);
}

static short v2_to_short_angle(const float v[2])
{
  return atan2f(v[1], v[0]) * float(M_1_PI) * SHRT_MAX;
}

static void edituv_get_edituv_stretch_angle(float auv[2][2],
                                            const float av[2][3],
                                            UVStretchAngle *r_stretch)
{
  /* Send UVs to the shader and let it compute the aspect corrected angle. */
  r_stretch->uv_angles[0] = v2_to_short_angle(auv[0]);
  r_stretch->uv_angles[1] = v2_to_short_angle(auv[1]);
  /* Compute 3D angle here. */
  r_stretch->angle = angle_normalized_v3v3(av[0], av[1]) * float(M_1_PI) * SHRT_MAX;

#if 0 /* here for reference, this is done in shader now. */
  float uvang = angle_normalized_v2v2(auv0, auv1);
  float ang = angle_normalized_v3v3(av0, av1);
  float stretch = fabsf(uvang - ang) / float(M_PI);
  return 1.0f - pow2f(1.0f - stretch);
#endif
}

static void extract_edituv_stretch_angle_init(const MeshRenderData &mr,
                                              MeshBatchCache & /*cache*/,
                                              void *buf,
                                              void *tls_data)
{
  gpu::VertBuf *vbo = static_cast<gpu::VertBuf *>(buf);
  static GPUVertFormat format = {0};
  if (format.attr_len == 0) {
    /* Waning: adjust #UVStretchAngle struct accordingly. */
    GPU_vertformat_attr_add(&format, "uv_angles", GPU_COMP_I16, 2, GPU_FETCH_INT_TO_FLOAT_UNIT);
    GPU_vertformat_attr_add(&format, "angle", GPU_COMP_I16, 1, GPU_FETCH_INT_TO_FLOAT_UNIT);
  }

  GPU_vertbuf_init_with_format(vbo, &format);
  GPU_vertbuf_data_alloc(vbo, mr.corners_num);

  MeshExtract_StretchAngle_Data *data = static_cast<MeshExtract_StretchAngle_Data *>(tls_data);
  data->vbo_data = (UVStretchAngle *)GPU_vertbuf_get_data(vbo);

  /* Special iterator needed to save about half of the computing cost. */
  if (mr.extract_type == MR_EXTRACT_BMESH) {
    data->cd_ofs = CustomData_get_offset(&mr.bm->ldata, CD_PROP_FLOAT2);
  }
  else {
    BLI_assert(mr.extract_type == MR_EXTRACT_MESH);
    data->uv = (const float2 *)CustomData_get_layer(&mr.mesh->corner_data, CD_PROP_FLOAT2);
  }
}

static void extract_edituv_stretch_angle_iter_face_bm(const MeshRenderData &mr,
                                                      const BMFace *f,
                                                      const int /*f_index*/,
                                                      void *_data)
{
  MeshExtract_StretchAngle_Data *data = static_cast<MeshExtract_StretchAngle_Data *>(_data);
  float(*auv)[2] = data->auv, *last_auv = data->last_auv;
  float(*av)[3] = data->av, *last_av = data->last_av;
  BMLoop *l_iter, *l_first;
  l_iter = l_first = BM_FACE_FIRST_LOOP(f);
  do {
    const int l_index = BM_elem_index_get(l_iter);

    const float(*luv)[2], (*luv_next)[2];
    BMLoop *l_next = l_iter->next;
    if (l_iter == BM_FACE_FIRST_LOOP(f)) {
      /* First loop in face. */
      BMLoop *l_tmp = l_iter->prev;
      BMLoop *l_next_tmp = l_iter;
      luv = BM_ELEM_CD_GET_FLOAT2_P(l_tmp, data->cd_ofs);
      luv_next = BM_ELEM_CD_GET_FLOAT2_P(l_next_tmp, data->cd_ofs);
      compute_normalize_edge_vectors(auv,
                                     av,
                                     *luv,
                                     *luv_next,
                                     bm_vert_co_get(mr, l_tmp->v),
                                     bm_vert_co_get(mr, l_next_tmp->v));
      /* Save last edge. */
      copy_v2_v2(last_auv, auv[1]);
      copy_v3_v3(last_av, av[1]);
    }
    if (l_next == BM_FACE_FIRST_LOOP(f)) {
      /* Move previous edge. */
      copy_v2_v2(auv[0], auv[1]);
      copy_v3_v3(av[0], av[1]);
      /* Copy already calculated last edge. */
      copy_v2_v2(auv[1], last_auv);
      copy_v3_v3(av[1], last_av);
    }
    else {
      luv = BM_ELEM_CD_GET_FLOAT2_P(l_iter, data->cd_ofs);
      luv_next = BM_ELEM_CD_GET_FLOAT2_P(l_next, data->cd_ofs);
      compute_normalize_edge_vectors(
          auv, av, *luv, *luv_next, bm_vert_co_get(mr, l_iter->v), bm_vert_co_get(mr, l_next->v));
    }
    edituv_get_edituv_stretch_angle(auv, av, &data->vbo_data[l_index]);
  } while ((l_iter = l_iter->next) != l_first);
}

static void extract_edituv_stretch_angle_iter_face_mesh(const MeshRenderData &mr,
                                                        const int face_index,
                                                        void *_data)
{
  MeshExtract_StretchAngle_Data *data = static_cast<MeshExtract_StretchAngle_Data *>(_data);
  const IndexRange face = mr.faces[face_index];

  const int corner_end = face.start() + face.size();
  for (int corner = face.start(); corner < corner_end; corner += 1) {
    float(*auv)[2] = data->auv, *last_auv = data->last_auv;
    float(*av)[3] = data->av, *last_av = data->last_av;
    int l_next = corner + 1;
    if (corner == face.start()) {
      /* First loop in face. */
      const int corner_last = corner_end - 1;
      const int l_next_tmp = face.start();
      compute_normalize_edge_vectors(auv,
                                     av,
                                     data->uv[corner_last],
                                     data->uv[l_next_tmp],
                                     mr.vert_positions[mr.corner_verts[corner_last]],
                                     mr.vert_positions[mr.corner_verts[l_next_tmp]]);
      /* Save last edge. */
      copy_v2_v2(last_auv, auv[1]);
      copy_v3_v3(last_av, av[1]);
    }
    if (l_next == corner_end) {
      l_next = face.start();
      /* Move previous edge. */
      copy_v2_v2(auv[0], auv[1]);
      copy_v3_v3(av[0], av[1]);
      /* Copy already calculated last edge. */
      copy_v2_v2(auv[1], last_auv);
      copy_v3_v3(av[1], last_av);
    }
    else {
      compute_normalize_edge_vectors(auv,
                                     av,
                                     data->uv[corner],
                                     data->uv[l_next],
                                     mr.vert_positions[mr.corner_verts[corner]],
                                     mr.vert_positions[mr.corner_verts[l_next]]);
    }
    edituv_get_edituv_stretch_angle(auv, av, &data->vbo_data[corner]);
  }
}

static GPUVertFormat *get_edituv_stretch_angle_format_subdiv()
{
  static GPUVertFormat format = {0};
  if (format.attr_len == 0) {
    /* Waning: adjust #UVStretchAngle struct accordingly. */
    GPU_vertformat_attr_add(&format, "angle", GPU_COMP_F32, 1, GPU_FETCH_FLOAT);
    GPU_vertformat_attr_add(&format, "uv_angles", GPU_COMP_F32, 2, GPU_FETCH_FLOAT);
  }
  return &format;
}

static void extract_edituv_stretch_angle_init_subdiv(const DRWSubdivCache &subdiv_cache,
                                                     const MeshRenderData &mr,
                                                     MeshBatchCache &cache,
                                                     void *buffer,
                                                     void * /*tls_data*/)
{
  gpu::VertBuf *refined_vbo = static_cast<gpu::VertBuf *>(buffer);

  GPU_vertbuf_init_build_on_device(
      refined_vbo, get_edituv_stretch_angle_format_subdiv(), subdiv_cache.num_subdiv_loops);

  gpu::VertBuf *pos_nor = cache.final.buff.vbo.pos;
  gpu::VertBuf *uvs = cache.final.buff.vbo.uv;

  /* It may happen that the data for the UV editor is requested before (as a separate draw update)
   * the data for the mesh when switching to the `UV Editing` workspace, and therefore the position
   * buffer might not be created yet. In this case, create a buffer it locally, the subdivision
   * data should already be evaluated if we are here. This can happen if the subsurf modifier is
   * only enabled in edit-mode. See #96338. */
  if (!pos_nor) {
    pos_nor = GPU_vertbuf_calloc();
    GPU_vertbuf_init_build_on_device(
        pos_nor, draw_subdiv_get_pos_nor_format(), subdiv_full_vbo_size(mr, subdiv_cache));

    draw_subdiv_extract_pos_nor(subdiv_cache, nullptr, pos_nor, nullptr);
  }

  /* UVs are stored contiguously so we need to compute the offset in the UVs buffer for the active
   * UV layer. */
  const CustomData *cd_ldata = (mr.extract_type == MR_EXTRACT_MESH) ? &mr.mesh->corner_data :
                                                                      &mr.bm->ldata;

  uint32_t uv_layers = cache.cd_used.uv;
  /* HACK to fix #68857 */
  if (mr.extract_type == MR_EXTRACT_BMESH && cache.cd_used.edit_uv == 1) {
    int layer = CustomData_get_active_layer(cd_ldata, CD_PROP_FLOAT2);
    if (layer != -1 && !CustomData_layer_is_anonymous(cd_ldata, CD_PROP_FLOAT2, layer)) {
      uv_layers |= (1 << layer);
    }
  }

  int uvs_offset = 0;
  for (int i = 0; i < MAX_MTFACE; i++) {
    if (uv_layers & (1 << i)) {
      if (i == CustomData_get_active_layer(cd_ldata, CD_PROP_FLOAT2)) {
        break;
      }

      uvs_offset += 1;
    }
  }

  /* The data is at `offset * num loops`, and we have 2 values per index. */
  uvs_offset *= subdiv_cache.num_subdiv_loops * 2;

  draw_subdiv_build_edituv_stretch_angle_buffer(
      subdiv_cache, pos_nor, uvs, uvs_offset, refined_vbo);

  if (!cache.final.buff.vbo.pos) {
    GPU_vertbuf_discard(pos_nor);
  }
}

constexpr MeshExtract create_extractor_edituv_edituv_stretch_angle()
{
  MeshExtract extractor = {nullptr};
  extractor.init = extract_edituv_stretch_angle_init;
  extractor.iter_face_bm = extract_edituv_stretch_angle_iter_face_bm;
  extractor.iter_face_mesh = extract_edituv_stretch_angle_iter_face_mesh;
  extractor.init_subdiv = extract_edituv_stretch_angle_init_subdiv;
  extractor.data_type = MR_DATA_NONE;
  extractor.data_size = sizeof(MeshExtract_StretchAngle_Data);
  extractor.use_threading = false;
  extractor.mesh_buffer_offset = offsetof(MeshBufferList, vbo.edituv_stretch_angle);
  return extractor;
}

/** \} */

const MeshExtract extract_edituv_stretch_angle = create_extractor_edituv_edituv_stretch_angle();

}  // namespace blender::draw
