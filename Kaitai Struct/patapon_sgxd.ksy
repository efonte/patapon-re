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
  #- id: audio
  #  size: header1.size_audio
instances:
  audios:
    type: audio(_index)
    repeat: expr
    repeat-expr: header2.sections[header2.sections[0].name == "RGND" ? 2 : 0].data.as<wave>.num_files
  
types:
  header1:
    seq:
    - id: size_sections # offset name
      type: u4
    - id: size_header # offset data
      type: u4
    - id: size_audio_raw
      type: u4
    instances:
      size_audio:
        value: size_audio_raw != 0 ? size_audio_raw - 0x80000000 : 0
      
  header2:
    seq:
      - id: sections
        type: section
        repeat: eos
        #repeat: expr
        #repeat-expr: 1
        
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
      #  repeat: expr
      #  repeat-expr: 28
      #- id: name
      #  type: strz
      #  encoding: shift-jis
  wave:
    seq:
      - id: unk1
        type: u4
      - id: num_files
        type: u4
      - id: waves
        type: wave_data
        repeat: expr
        repeat-expr: num_files
  
  wave_data:
    seq:
      - id: unk1
        type: u4
      - id: name_offset
        type: u4
      - id: file_format
        type: u1
      - id: channels
        type: u1
      - id: unk2
        type: u2
      - id: playback_frequency
        type: u4
      - id: bitrate
        type: u4
      - id: data_size
        type: u4
      - id: unk3
        type: u4
      - id: unk4
        type: u4
      - id: total_samples
        type: u4
      - id: loop_beg
        type: u4
      - id: loop_end
        type: u4
      - id: size_audio
        type: u4
      - id: unk6
        type: u4
      - id: sgd_data_size
        type: u4
      
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
      - id: file_index
        type: u2
      - id: name_type
        type: u2
      - id: name_offset
        type: u2
      - id: unk4 # padding?
        type: u2
  
  audio:
    params:
      - id: i
        type: s4
    seq:
      - id: data
        size: _parent.header2.sections[_parent.header2.sections[0].name == "RGND" ? 2 : 0].data.as<wave>.waves[i].size_audio
    
