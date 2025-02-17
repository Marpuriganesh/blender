/* SPDX-License-Identifier: GPL-2.0-or-later
 * Copyright 2005 Blender Foundation */

#include "node_shader_util.hh"

namespace blender::nodes::node_shader_background_cc {

static void node_declare(NodeDeclarationBuilder &b)
{
  b.add_input<decl::Color>(N_("Color")).default_value({0.8f, 0.8f, 0.8f, 1.0f});
  b.add_input<decl::Float>(N_("Strength")).default_value(1.0f).min(0.0f).max(1000000.0f);
  b.add_input<decl::Float>(N_("Weight")).unavailable();
  b.add_output<decl::Shader>(N_("Background"));
}

static int node_shader_gpu_background(GPUMaterial *mat,
                                      bNode *node,
                                      bNodeExecData * /*execdata*/,
                                      GPUNodeStack *in,
                                      GPUNodeStack *out)
{
  return GPU_stack_link(mat, node, "node_background", in, out);
}

}  // namespace blender::nodes::node_shader_background_cc

/* node type definition */
void register_node_type_sh_background()
{
  namespace file_ns = blender::nodes::node_shader_background_cc;

  static bNodeType ntype;

  sh_node_type_base(&ntype, SH_NODE_BACKGROUND, "Background", NODE_CLASS_SHADER);
  ntype.declare = file_ns::node_declare;
  ntype.add_ui_poll = world_shader_nodes_poll;
  ntype.gpu_fn = file_ns::node_shader_gpu_background;

  nodeRegisterType(&ntype);
}
