/* SPDX-License-Identifier: GPL-2.0-or-later
 * Copyright 2022 Blender Foundation */

/** \file
 * \ingroup gpu
 */

#pragma once

#include "gpu_index_buffer_private.hh"

#include "vk_buffer.hh"

namespace blender::gpu {

class VKIndexBuffer : public IndexBuf {
  VKBuffer buffer_;

 public:
  void upload_data() override;

  void bind_as_ssbo(uint binding) override;
  void bind(VKContext &context);

  void read(uint32_t *data) const override;

  void update_sub(uint start, uint len, const void *data) override;

  VkBuffer vk_handle() const
  {
    return buffer_.vk_handle();
  }

 private:
  void strip_restart_indices() override;
  void allocate();
  void ensure_updated();
};

static inline VKIndexBuffer *unwrap(IndexBuf *index_buffer)
{
  return static_cast<VKIndexBuffer *>(index_buffer);
}

}  // namespace blender::gpu
