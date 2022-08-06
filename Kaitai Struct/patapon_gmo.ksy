meta:
  id: patapon_gmo
  file-extension: gmo
  endian: le
  title: Patapon (gmo)
seq:
  - id: header
    type: header
  - id: chunks
    type: chunk

types:
  header:
    seq:
      - id: magic
        contents: ["OMG.00.1PSP"]
      - id: padding1
        size: 5

  chunk:
    seq:
      - id: type
        type: u2
        #enum: chunk_type
      - id: size_header
        type: u2
      - id: size
        type: u4
      - id: body
        type:
          switch-on: type
          cases:
            0x0002: chunk_0002_root
            0x0003: chunk_0003_model
            0x0004: chunk_0004_bone
            0x0005: chunk_0005_part
            0x0006: chunk_0006_mesh
            0x0007: chunk_0007_arrays
            0x0008: chunk_0008_material
            0x0009: chunk_0009_layer
            0x000A: chunk_000a_texture
            0x000B: chunk_000b_motion
            0x000C: chunk_000c_fcurve
            0x000F: chunk_000f_blind_block
            0x8012: chunk_8012_texture_file_name
            0x8013: chunk_8013_texture
            0x8014: chunk_8014_bounding_box
            0x8015: chunk_8015
            0x8041: chunk_8041_parent_bone
            0x8042: chunk_8042_visibility
            0x8045: chunk_8045_blend_offsets
            0x8044: chunk_8044_blend_bones
            0x8048: chunk_8048_translate
            0x804B: chunk_804b_rotate_q
            0x804E: chunk_804e_draw_part
            0x8061: chunk_8061_set_material
            0x8062: chunk_8062_blend_subset
            0x8066: chunk_8066_draw_arrays
            0x8082: chunk_8082_material_diffuse
            0x8083: chunk_8083_material_specular
            0x8085: chunk_8085_material_ambient
            0x8091: chunk_8091_material_layer
            0x80B1: chunk_80b1_frame_loop
            0x80B2: chunk_80b2_frame_rate
            0x80B3: chunk_80b3_animate
            0x80B4: chunk_80b4_frame_repeat
            0x80E2: chunk_80e2_bone_state
            0x80F1: chunk_80f1_blind_data
            _: chunk_unknown
        size: size - 8
        #size-eos: true

  chunk_unknown:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0
      - id: body
        #type: chunk
        size: "_parent.size_header != 0 ? _parent.size - _parent.size_header : _parent.size - 8"
        #repeat: eos
        #size-eos: true

  chunk_0002_root:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0
      - id: body
        type: chunk
        #size: _parent.size - _parent.size_header
        #repeat: eos
        #size-eos: true

  chunk_0003_model:
    seq:
      - id: header
        size: 8
      - id: header_name
        type: str
        encoding: utf-8
        size: _parent.size_header - 8 - 8
      - id: body_chunks
        type: chunk
        repeat: eos

  chunk_0004_bone:
    seq:
      - id: header
        size: 8
      - id: header_name
        type: str
        encoding: utf-8
        size: _parent.size_header - 8 - 8
      - id: body_chunks
        type: chunk
        repeat: eos

  chunk_000b_motion:
    seq:
      - id: header
        size: 8
      - id: header_name
        type: str
        encoding: utf-8
        size: _parent.size_header - 8 - 8
      - id: body_chunks
        type: chunk
        repeat: eos

  chunk_0005_part:
    seq:
      - id: header
        size: 8
      - id: header_name
        type: str
        encoding: utf-8
        size: _parent.size_header - 8 - 8
      - id: body_chunks
        type: chunk
        repeat: eos

  chunk_0006_mesh:
    seq:
      - id: header
        size: 8
      - id: header_name
        type: str
        encoding: utf-8
        size: _parent.size_header - 8 - 8
      - id: body_chunks
        type: chunk
        repeat: eos

  chunk_0007_arrays:
    seq:
      - id: header
        size: 8
      - id: header_name
        type: str
        encoding: utf-8
        size: _parent.size_header - 8 - 8
      - id: arrays_type
        type: u4
      - id: arrays_value1
        type: u4
      - id: arrays_value2
        type: u4
      - id: arrays_value3
        type: u4
      - id: values
        type: f4
        repeat: expr
        repeat-expr: (_parent.size - _parent.size_header - 4 * 4) / 4

  chunk_0008_material:
    seq:
      - id: header
        size: 8
      - id: header_name
        type: str
        encoding: utf-8
        size: _parent.size_header - 8 - 8
      - id: body_chunks
        type: chunk
        repeat: eos

  chunk_0009_layer:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0
      - id: body_chunks
        type: chunk
        repeat: eos

  chunk_000a_texture:
    seq:
      - id: header
        size: 8
      - id: header_name
        type: str
        encoding: utf-8
        size: _parent.size_header - 8 - 8
      - id: body_chunks
        type: chunk
        repeat: eos

  chunk_000c_fcurve:
    seq:
      - id: header
        size: 8
      - id: header_name
        type: str
        encoding: utf-8
        size: _parent.size_header - 8 - 8
      - id: fcurve_type
        type: u4
        enum: fcurve_type
      - id: fcurve_value1
        type: u4
      - id: fcurve_value2
        type: u4
      - id: fcurve_value3
        type: u4
      - id: values
        #type: f4
        #repeat: expr
        #repeat-expr: (_parent.size - _parent.size_header - 4 * 4) / 4
        type: u2
        repeat: eos
    enums:
      fcurve_type:
        0x80: constant
        0x81: linear
        0x82: hermite
        0x84: spherical

  chunk_000f_blind_block:
    seq:
      - id: header
        size: 8
      - id: header_name
        type: str
        encoding: utf-8
        size: _parent.size_header - 8 - 8
      - id: body_chunks
        type: chunk
        repeat: eos

  chunk_8012_texture_file_name:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: name
        type: str
        encoding: utf-8
        size-eos: true

  chunk_8013_texture:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: texture
        size-eos: true

  chunk_8014_bounding_box:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: value1
        type: f4
      - id: value2
        type: f4
      - id: value3
        type: f4
      - id: value4
        type: f4
      - id: value5
        type: f4
      - id: value6
        type: f4

  chunk_8015:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: value1
        type: u4
      - id: values
        type: f4
        repeat: eos

  chunk_8041_parent_bone:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: value1
        type: u4

  chunk_8042_visibility:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: value1
        type: u4

  chunk_8044_blend_bones:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: value1
        type: u4
      - id: values
        type: u4
        repeat: eos

  chunk_8045_blend_offsets:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: value1
        type: u4
      - id: values
        type: f4
        repeat: eos

  chunk_8048_translate:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: value1
        type: f4
      - id: value2
        type: f4
      - id: value3
        type: f4

  chunk_804b_rotate_q:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: value1
        type: f4
      - id: value2
        type: f4
      - id: value3
        type: f4
      - id: value4
        type: f4

  chunk_804e_draw_part:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: value1
        type: u4

  chunk_8061_set_material:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: value1
        type: u4

  chunk_8062_blend_subset:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: num_values
        type: u4
      - id: values
        type: u4
        repeat: expr
        repeat-expr: num_values

  chunk_8066_draw_arrays:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: value1
        type: u4
      - id: type
        type: u4
        enum: draw_arrays_type
      - id: value2
        type: u4
      - id: value3
        type: u4
      - id: values
        type: u2
        repeat: eos
    enums:
      draw_arrays_type:
        0x3: triangles
        0x4: triangle_strip

  chunk_8082_material_diffuse:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0
      - id: value1_raw
        type: u1
      - id: value2_raw
        type: u1
      - id: value3_raw
        type: u1
      - id: value4_raw
        type: u1
    instances:
      value1:
        value: (value1_raw / 255.0)
      value2:
        value: (value2_raw / 255.0)
      value3:
        value: (value3_raw / 255.0)
      value4:
        value: (value4_raw / 255.0)

  chunk_8083_material_specular:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0
      - id: value1_raw
        type: u1
      - id: value2_raw
        type: u1
      - id: value3_raw
        type: u1
      - id: value4_raw
        type: u1
      - id: value5
        type: f4
    instances:
      value1:
        value: (value1_raw / 255.0)
      value2:
        value: (value2_raw / 255.0)
      value3:
        value: (value3_raw / 255.0)
      value4:
        value: (value4_raw / 255.0)

  chunk_8085_material_ambient:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0
      - id: value1_raw
        type: u1
      - id: value2_raw
        type: u1
      - id: value3_raw
        type: u1
      - id: value4_raw
        type: u1
    instances:
      value1:
        value: (value1_raw / 255.0)
      value2:
        value: (value2_raw / 255.0)
      value3:
        value: (value3_raw / 255.0)
      value4:
        value: (value4_raw / 255.0)

  chunk_8091_material_layer:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0
      - id: value1
        type: u4

  chunk_80b1_frame_loop:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0
      - id: value1
        type: f4
      - id: value2
        type: f4

  chunk_80b2_frame_rate:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0
      - id: value1
        type: f4

  chunk_80b3_animate:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0
      - id: value1
        type: u4
      - id: type
        type: u4
        enum: animate_type
      - id: value3
        type: u4
      - id: value4
        type: u4
    enums:
      animate_type:
        0x48: translate
        0x4B: rotate_q
        0x4D: scale2

  chunk_80b4_frame_repeat:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0
      - id: type
        type: u4
        enum: frame_repeat_type
    enums:
      frame_repeat_type:
        0x0: hold
        0x1: cycle

  chunk_80e2_bone_state:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: value1
        type: u4
      - id: value2
        type: u4
      - id: unk1 # padding?
        size-eos: true

  chunk_80f1_blind_data:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0
      - id: name
        type: strz
        encoding: utf-8
      - id: name_padding
        size: "(name.length+1) % 4 == 0 ? 0 : 4 + ((name.length+1) / 4) * 4 - (name.length+1)"
      - id: values
        type: u4
        repeat: eos
