meta:
  id: patapon_sgxd
  file-extension: sgd
  endian: le
  title: Patapon (sgxd)
seq:
  - id: magic
    contents: ['SGXD']
  - id: header1
    type: header1
  - id: header2
    type: header2
    size: header1.size_header - 16
  - id: audio
    size: header1.size_audio

types:
  header1:
    seq:
    - id: size_sections
      type: u4
    - id: size_header
      type: u4
    - id: size_audio_raw
      type: u4
    instances:
      size_audio:
        value: size_audio_raw - 0x80000000
      
  header2:
    seq:
      - id: sections
        type: section
        repeat: eos
        
  section:
    seq:
      - id: name
        type: str
        encoding: utf-8
        size: 4
      - id: size
        type: u4
      - id: data
        type:
          switch-on: name
          cases:
            '"RGND"': rgnd
            '"SEQD"': seqd
            '"WAVE"': wave
            '"NAME"': name
            _: unk_section
        size: size
      
  unk_section:
    seq:
      - id: data
        size-eos: true

  rgnd:
    seq:
      - id: values
        type: u2
        repeat: eos
  
  seqd:
    seq:
      - id: values
        type: u2
        repeat: eos
  
  wave:
    seq:
      - id: values
        type: u2
        repeat: eos
  
  name:
    seq:
      - id: unk1
        type: u4
      - id: num_names
        type: u4
      - id: values
        type: name_data
        repeat: expr
        repeat-expr: num_names
      - id: names
        type: strz
        encoding: utf-8
        repeat: expr
        repeat-expr: num_names
      - id: padding
        size-eos: true
  
  name_data:
    seq:
      - id: unk1
        type: u2
      - id: unk2
        type: u2
      - id: unk3
        type: u2
      - id: unk4
        type: u2
