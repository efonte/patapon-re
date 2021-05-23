meta:
  id: patapon_msg
  file-extension: msg
  endian: le
  title: Patapon (msg)
seq:
  - id: num_texts
    type: u4
  - id: unk
    type: u4
  - id: offsets
    type: u4
    repeat: expr
    repeat-expr: num_texts
  - id: padding
    type: u4
instances:
    texts:
      type: texts(_index)
      repeat: expr
      repeat-expr: num_texts

types:
  texts:
    params:
      - id: i
        type: s4
    instances:
      text:
        pos: _parent.offsets[i]
        type: str
        encoding: UTF-16
        size: i+1 < _parent.offsets.size ? _parent.offsets[i+1] - _parent.offsets[i] : _io.size - _parent.offsets[i]

