meta:
  id: cyacd2_file
  file-extension: cyacd2
  ks-version: 0.9
  ks-opaque-types: true
  endian: le
seq:
  - id: header
    type: header
  - id: app_info
    type: app_info
  - id: data_rows
    type: data_row
    repeat: eos
    # repeat: expr
    # repeat-expr: 2
types:
  header:
    seq:
      - id: header_str
        type: str
        terminator: 0x0A
        eos-error: false
        encoding: ASCII
    instances:
      file_version:
        value: header_str.substring(0, 2).to_i(16)
      silicon_id:
        value: header_str.substring(2, 10).to_i(16)
      silicon_rev:
        value: header_str.substring(10, 12).to_i(16)
      checksum_type:
        value: header_str.substring(12, 14).to_i(16)
      app_id:
        value: header_str.substring(14, 16).to_i(16)
      product_id:
        value: header_str.substring(16, 25).to_i(16)
  app_info:
    seq:
      - id: magic
        contents: '@APPINFO:'
      - id: start_address_str
        type: str
        terminator: 0x2C
        eos-error: false
        encoding: ASCII
      - id: length_str
        type: str
        terminator: 0x0A
        eos-error: false
        encoding: ASCII
    instances:
      start_address:
        value: start_address_str.to_i(16)
      length:
        value: length_str.to_i(16)
  data_row:
    seq:
      - id: header
        contents: ':'
      - id: address_str
        type: str
        size: 8
        encoding: ASCII
      - id: data
        type: HexString
    instances:
      address_0:
        value: address_str.substring(0, 2).to_i(16)
      address_1:
        value: address_str.substring(2, 4).to_i(16)
      address_2:
        value: address_str.substring(4, 6).to_i(16)
      address_3:
        value: address_str.substring(6, 8).to_i(16)
      address:
        value: address_0 | (address_1 << 8) | (address_2 << 16) | (address_3 << 24)

