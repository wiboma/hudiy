# Description

This directory contains the translation file for the texts used in Hudiy. You can use it to translate the interface into your desired language.

The most convenient way to edit  `*.ts` files is by using the `linguist` tool located in `/usr/lib/qt6/bin/`

To generate release files (`*.qm`), run:

```bash
/usr/lib/qt6/bin/lrelease hudiy.ts -qm hudiy.qm
```

To install the `linguist` and `lrelease` tools, use the following command:

```bash
sudo apt install -y linguist-qt6 qt6-l10n-tools
```

Once generated, the `*.qm` translation file can be referenced in `main_configuration.json` to enable the selected language in Hudiy.
