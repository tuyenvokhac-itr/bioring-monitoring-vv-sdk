meta:
  id: psoc6_dfu_command_packet
  endian: le
seq:
  - id: sop
    contents: [0x01]
  - id: command
    type: u1
    enum: dfu_command
  - id: len_data
    type: u2
  - id: data
    size: len_data
    type:
      switch-on: command
      cases:
        'dfu_command::enter': product_id
        'dfu_command::sync': empty_data
        'dfu_command::exit': empty_data
        'dfu_command::program_data': program_data(len_data-8)
        'dfu_command::verify_data': verify_data(len_data-8)
        'dfu_command::erase_data': erase_data
        'dfu_command::verify_app': u1
        'dfu_command::set_app_metadata': set_app_metadata
        'dfu_command::get_metadata': get_metadata
  - id: checksum
    type: u2
  - id: eop
    contents: [0x17]
types:
  empty_data:
    doc: empty_data type for commands that don't have data
  product_id:
    seq:
      - id: magic
        contents: [ 0x04, 0x03, 0x02, 0x01 ]
  program_data:
    params:
      - id: len_data
        type: u2
    seq:
      - id: address
        type: u4
      - id: crc # CRC-32C of data
        type: u4
      - id: data
        size: len_data
  verify_data:
    params:
      - id: len_data
        type: u2
    seq:
      - id: address
        type: u4
      - id: crc # CRC-32C of data
        type: u4
      - id: data
        size: len_data
  erase_data:
    seq:
      - id: address
        type: u4
  app_metadata:
    seq:
      - id: start_address
        type: u4
      - id: length
        type: u4
  set_app_metadata:
    seq:
      - id: app_id
        type: u1
      - id: app_metadata
        type: app_metadata
  get_metadata:
    seq:
      - id: from_offset
        type: u2
      - id: to_offset
        type: u2
enums:
  dfu_command:
    0x38: enter
    0x35: sync
    0x3B: exit
    0x37: send_data
    0x47: send_data_no_resp
    0x49: program_data
    0x4A: verify_data
    0x44: erase_data
    0x31: verify_app
    0x4C: set_app_metadata
    0x3C: get_metadata
    0x4D: set_eivector
