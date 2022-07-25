meta:
  id: patapon_squadlineparam
  file-extension: dat
  endian: le
  title: Patapon (squadlineparam)
seq:
  - id: header
    type: header

types:
  header:
    seq:
      - id: magic
        contents: ["YGF_GFP", 0]
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
      - id: unk8
        type: s4
      - id: num_params
        type: s4
      - id: size_param
        type: s4
      - id: unk11
        type: s4
      - id: unk12
        type: s4
      - id: unk13
        type: s4
      - id: unk14
        type: s4
      - id: base_param
        type: strz
        encoding: utf-8
        size: 0x20
      - id: unk15
        type: s4
      - id: unk16
        type: s4
      - id: unk17
        type: f4
      - id: unk18
        type: f4
      - id: unk19
        type: s4
      - id: unk20
        type: s4
      - id: unk21
        type: s4
      - id: unk22
        type: s4
      - id: params
        type: param
        repeat: expr
        repeat-expr: num_params

  param:
    seq:
      #- id: data
      #  size: 0x100
      - id: name
        type: strz
        encoding: utf-8
        size: 0x20
      - id: unk1
        type: s4
      - id: unk2
        type: s4
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
      - id: unk8
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
      - id: unk15
        type: s4
      - id: unk16
        type: s4
      - id: unk17
        type: s4
      - id: unk18
        type: s4
      - id: unk19
        type: s4
      - id: unk20
        type: s4
      - id: unk21
        type: s4
      - id: unk22
        type: s4
      - id: unk23
        type: s4
      - id: unk24
        type: s4
      - id: unk25
        type: s4
      - id: unk26
        type: s4
      - id: unk27
        type: s4
      - id: unk28
        type: s4
      - id: unk29
        type: s4
      - id: unk30
        type: s4
      - id: unk31
        type: s4
      - id: unk32
        type: s4
      - id: unk33
        type: s4
      - id: unk34
        type: s4
      - id: unk35
        type: s4
      - id: unk36
        type: s4
      - id: unk37
        type: s4
      - id: unk38
        type: s4
      - id: unk39
        type: s4
      - id: unk40
        type: s4
      - id: unk41
        type: s4
      - id: unk42
        type: s4
      - id: unk43
        type: s4
      - id: unk44
        type: s4
      - id: unk45
        type: s4
      - id: unk46
        type: s4
      - id: unk47
        type: s4
      - id: unk48
        type: s4
      - id: unk49
        type: s4
      - id: unk50
        type: s4
      - id: unk51
        type: s4
      - id: unk52
        type: s4
      - id: unk53
        type: s4
      - id: unk54
        type: s4
      - id: unk55
        type: s4
      - id: unk56
        type: s4
