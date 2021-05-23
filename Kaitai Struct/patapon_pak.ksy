meta:
  id: patapon_pak
  file-extension: pak
  endian: le
  title: Patapon PS4 (pak)
seq:
  - id: header
    type: header
  - id: entries
    type: entry
    repeat: expr
    repeat-expr: header.num_entries
 
types:
  header:
    seq:
      - id: magic
        contents: ['PAKF']
      - id: padding1
        size: 4
      - id: num_entries
        type: u4
      - id: padding2
        size: 4
      
  entry:
    seq:
      - id: name
        type: strz
        size: 0x40
        encoding: utf-8
      - id: width
        type: u4
      - id: height
        type: u4
      - id: size
        type: u4
      - id: size_pixels
        type: u4



