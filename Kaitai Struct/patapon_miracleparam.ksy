meta:
  id: patapon_miracleparam
  file-extension: dat
  endian: le
  title: Patapon (miracleparam)
seq:
  - id: header
    type: header

types:
  header:
    seq:
      - id: magic
        contents: ['YGF_GFP', 0]
      - id: unk1 # size header or offset baseparam
        type: s4
      - id: unk2
        type: f4
      - id: unk3
        type: s4
      - id: unk4
        type: s4
      - id: unk5
        type: s4
      - id: unk6
        type: s4
      - id: unk7
        type: s4
      - id: param_size
        type: s4
      - id: unk9
        type: s4
      - id: unk10
        type: s4
      - id: unk11
        type: s4
      - id: unk12
        type: s4
      - id: unk13
        type: s4
      - id: unk14
        type: s4
      - id: params
        type: param
        #repeat: expr
        #repeat-expr: 2
        repeat: eos

  param:
    seq:
      - id: name
        type: strz
        encoding: shift-jis
        size: 0x20
      - id: unk1
        type: s4
      - id: unk2
        type: s4
      - id: file_name
        type: strz
        encoding: shift-jis
        size: 0x20
      - id: model_name
        type: strz
        encoding: shift-jis
        size: 0x20
        if: _parent.param_size == 0x68
  