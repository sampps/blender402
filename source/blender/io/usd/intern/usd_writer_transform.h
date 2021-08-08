/*
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 * The Original Code is Copyright (C) 2019 Blender Foundation.
 * All rights reserved.
 */
#pragma once

#include "usd_writer_abstract.h"

#include <pxr/usd/usdGeom/xform.h>

#include <vector>

namespace blender::io::usd {

class USDTransformWriter : public USDAbstractWriter {
 private:
  std::vector<pxr::UsdGeomXformOp> xformOps_;

 public:
  USDTransformWriter(const USDExporterContext &ctx);

 protected:
  void do_write(HierarchyContext &context) override;
  bool check_is_animated(const HierarchyContext &context) const override;

  void set_xform_ops(float parent_relative_matrix[4][4], pxr::UsdGeomXformable &xf);

  /* Return true if the given context is the root of a protoype. */
  bool is_proto_root(const HierarchyContext &context) const;

  /* Subclasses may override this to create prims other than UsdGeomXform. */
  virtual pxr::UsdGeomXformable create_xformable() const;

  bool should_apply_root_xform(const HierarchyContext &context) const;
};

}  // namespace blender::io::usd
