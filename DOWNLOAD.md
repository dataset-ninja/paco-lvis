Dataset **PACO-LVIS** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/l/c/Ok/aRTODhjFg7AOyz1CzsZBP4bNdhmoToYpx0R8CfnbDGoRhipbSmfjJPHVWzwYeACPhCu9KrMKJu33IAsocOy0vToTtH8nJWpb0EAET3QJDqMwuU3z9UXQVagpIQI9.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='PACO-LVIS', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

