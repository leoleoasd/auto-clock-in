## Introduction

A auto clock-in script based on python3 for BJUTer.

It could clock in at 9:00 a.m everyday.

> The script is inspired by [tsosunchia](https://github.com/tsosunchia/bjut_autosignin)

## What can I do ?

- [x] Clock in at 9:00 a.m everyday
- [x] Send the email after clocking in

## Usage

1. Fork the project 

2. Settings
    Open the settings in your forking repository, add the following info to your secrets.

    ```
    EMAIL_USERNAME 
    EMAIL_FROM # usually equal to EMAIL_USERNAME
    EMAIL_TO # usually equal to EMAIL_USERNAME
    EMAIL_PASSWORD 
    EMAIL_SERVER
    EMAIL_PORT
    DATA
    ```

## Test
Run the script
```shell
python3 app.py
```

## Example

  Inspired by [tsosunchia](https://github.com/tsosunchia/bjut_autosignin)，I extract the user info module as a single file, which is easy for us to update own info.

  A example of `DATA` is listed as below.

  ```json
{
  "id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "c16": "在校且住宿",
  "c17": "在京",
  "c18": "低风险地区",
  "c12": "北京市,北京市,朝阳区,",
  "c15": "无情况",
  "type": "YQSJSB",
  "location_longitude": 116.480165,
  "location_latitude": 39.873745,
  "location_address": "北京市朝阳区南磨房乡北京工业大学"
}
  ```

  ## Thanks
  ✨ [Woodykaixa](https://github.com/Woodykaixa)
  ✨ [galaxyxxxxx](https://github.com/galaxyxxxxx)
