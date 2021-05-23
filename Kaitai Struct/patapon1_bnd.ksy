meta:
  id: patapon1_bnd
  file-extension: bnd
  endian: le
  title: Patapon (bnd)
seq:
  - id: header
    type: header
  #- id: asd
  #  type: asd
    #pos: header.offset_info
    #repeat: until
    #repeat-until: 
    #repeat: expr
    #repeat-expr: 4
  #- id: names
  #  type: str
  #  encoding: UTF-8
  #  terminator: 0
  #  repeat: eos
  #- id: name
  #  type: str
  #  encoding: UTF-8
  #  size: 36
  #- id: id
  #  type: u4
  #- id: unk1
  #  type: u4
  #- id: unk2
  #  type: u4
    

types:
  header:
    seq:
      - id: magic
        contents: ['BND', 0]
      - id: unk1
        type: u4
      - id: unk2
        type: u4
      - id: unk3
        type: u4
      - id: offset_info
        type: u4
      - id: offset_files
        type: u4
      - id: unk4
        type: u4
      - id: unk5
        type: u4
      - id: files
        type: u4
      - id: entries
        type: u4
      #- id: version
      #  type: str
      #  encoding: UTF-8
      #  size: 4
      #- id: num_images
      #  type: u4
      #- id: images
      #  type: image
    instances:
      data:
        pos: offset_info
        type: data1
          
  data1:
    seq:
      - id: folder_level
        type: s1
      - id: dummy_level
        type: s1
      - id: next_size
        type: s1
      - id: offset
        type: u4
      - id: name
        type: str
        encoding: UTF-8
        terminator: 0
    instances:
      subdata:
        pos: offset
        type: data2
      #- id: width
      #  type: u4
      #- id: height
      #  type: u4
      #- id: palette
      #  type: rgb
      #  repeat: expr
      #  repeat-expr: 256
      
  data2:
    seq:
      - id: crc
        type: u4
      - id: ofsset2_info
        type: u4
      - id: offset
        type: u4
      - id: size
        type: u4
    instances:
      name:
        value: _parent.folder_level * -1 - 1
        #if: _parent.folder_level >= 0
      #name1:
      #  value: 2
      #  if: _parent.folder_level < 0
        
  rgb:
    seq:
      - id: red
        type: u1
      - id: green
        type: u1
      - id: blue
        type: u1
    -webide-representation: "rgb({red:dec}, {green:dec}, {blue:dec})"
    
  file:
    seq:
      - id: name
        type: str
        encoding: UTF-8
        size: 36
      - id: type
        type: u4
        enum: file_type
      #- id: is_file
      #  type: b1
      #- id: padding
      #  size: 3
      - id: size
        type: s4
      - id: offset
        type: s4
      #- id: file
      #  type:
      #    switch-on: type
      #    cases:
      #      file_type::file: file
      #      file_type::directory: directory
      #      #file_type::directory_end: directory_end
      #- id: files
      #  type: header
      #  repeat: expr
      #  repeat-expr: num_files
      #  if: type == file_type::directory

    enums:
      file_type:
        0x0: file
        0x1: directory
        0xFF: directory_end
        
    instances:
      files:
        #io: _root._io
        #io: _io
        pos: offset
        type: file
        repeat: until
        repeat-until: _.type == file_type::directory_end
        if: type == file_type::directory
        #if: type == file_type::directory and type != file_type::directory_end
        
    #    #size: offset - _io.pos
    #    #repeat: eos
    #    repeat: expr
    #    repeat-expr: 3
    #    #repeat-expr:  303
    #    #repeat-expr: offset
    #    #repeat: until
    #    #repeat-until: _root._io.pos <= offset
    #    #if: is_file == false
    #  #a:
      #  value: _io.pos
      #b:
      #  value: _io.pos <= offset
      data:
        #io: _root._io
        pos: offset
        size: size
        if: type == file_type::file 
