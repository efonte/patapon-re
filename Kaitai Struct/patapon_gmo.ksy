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
        contents: ['OMG.00.1PSP']
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
            0x0005: chunk_0005
            0x0006: chunk_0006
            0x0007: chunk_0007
            0x0008: chunk_0008_material
            0x0009: chunk_0009
            0x000A: chunk_000a_texture
            0x000B: chunk_000b
            0x000C: chunk_000c_fcurve
            0x000F: chunk_000f
            0x8012: chunk_8012_texture_file_name
            0x8013: chunk_8013_texture
            0x8014: chunk_8014_bounding_box
            0x8041: chunk_8041
            0x8042: chunk_8042_visibility
            0x8045: chunk_8045
            0x8044: chunk_8044
            0x8048: chunk_8048_translate
            0x804B: chunk_804b_rotate_q
            0x804E: chunk_804e
            0x8061: chunk_8061
            0x8066: chunk_8066
            0x8082: chunk_8082_material
            0x8083: chunk_8083_material_specular
            0x8085: chunk_8085_material
            0x8091: chunk_8091
            0x80B1: chunk_80b1
            0x80B2: chunk_80b2
            0x80B3: chunk_80b3
            0x80E2: chunk_80e2_bone_state
            0x80F1: chunk_80f1
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
        size: '_parent.size_header != 0 ? _parent.size - _parent.size_header : _parent.size - 8'
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
      
  chunk_000b:
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
  
  chunk_0005:
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
  
  chunk_0006:
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
        
  chunk_0007:
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
  
  chunk_0009:
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
      - id: fcurve_value1
        type: u4
      - id: fcurve_value2
        type: u4
      - id: fcurve_value3
        type: u4
      - id: values
        type: f4
        repeat: expr
        repeat-expr: (_parent.size - _parent.size_header - 4 * 4) / 4
  
  chunk_000f:
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
  
  chunk_8041:
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
        
  chunk_8044:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0 
      - id: value1
        type: u4
      - id: values
        type: u4
        repeat: eos
  
  chunk_8045:
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
  
  chunk_804e:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0 
      - id: value1
        type: u4
        
  chunk_8061:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0 
      - id: value1
        type: u4
        
  chunk_8066:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0 
      - id: value1
        type: u4
      - id: type
        type: u2
        enum: draw_arrays_type
      - id: value2
        type: u2
      - id: value3
        type: u4
      - id: value4
        type: u4
      - id: values
        type: u2
        repeat: eos
    enums:
      draw_arrays_type:
        0x3: triangles
        0x4: triangle_strip
        
  chunk_8082_material:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0 
      - id: value1
        type: u1
      - id: value2
        type: u1
      - id: value3
        type: u1
      - id: value4
        type: u1
        
  chunk_8083_material_specular:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0 
      - id: value1
        type: u1
      - id: value2
        type: u1
      - id: value3
        type: u1
      - id: value4
        type: u1
      - id: value5
        type: f4
        
  chunk_8085_material:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0 
      - id: value1
        type: u1
      - id: value2
        type: u1
      - id: value3
        type: u1
      - id: value4
        type: u1
  
  chunk_8091:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0 
      - id: value1
        type: u4
       
  chunk_80b1:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0 
      - id: value1
        type: f4
      - id: value2
        type: f4
  
  chunk_80b2:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0 
      - id: value1
        type: f4
  
  chunk_80b3:
    seq:
      - id: header
        size: _parent.size_header - 8
        if: _parent.size_header != 0 
      - id: value1
        type: u4
      - id: value2
        type: u4
      - id: value3
        type: u4
      - id: value4
        type: u4
        
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
        
  chunk_80f1:
    seq:
      #- id: header
      #  size: _parent.size_header - 8
      #  if: _parent.size_header != 0 
      - id: name
        type: strz
        encoding: utf-8
      #- id: name_paddiing
      #  size: 'name.len % 4 == 0 ? 0 : 4 + (name.len / 4) * 4 - name.len'
      # TODO read padding
      - id: values
      #  type: u4
        size-eos: true
  