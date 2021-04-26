# WoTDL Ontology to REST

## Overview
This toolchain allows to generate REST APIs from instances of the [WoTDL OWL Ontology](https://vsr.informatik.tu-chemnitz.de/projects/2019/growth/wotdl/wotdl.owl), which is part of the GrOWTH approach for Goal-Oriented End User Development for Web of Things Devices. [1] WoTDL has been listed on the [LOV4IoT Ontology Catalogue](http://lov4iot.appspot.com/?p=ontologies).

It uses a model-to-model transformation to generate an [OpenAPI](https://openapis.org) specification. 
The Flask-based REST API is generated using [OpenAPI Generator](https://openapi-generator.tech).

## Requirements
- Python 3.7.0+
- for python requirements see requirements.txt
- openapi-generator 3.3.4+

## Usage
Get the dependencies:
```
pipenv install
pipenv shell
```

Adapt the IN variable to point to your ontology instance and run the model-to-model transformation:

```
python m2m_openapi.py
```

Run the model-to-text generation:

```
./m2t_openapi_flask.sh
```


## References
If you want to use or extend our toolchain, please consider citing the related publications:

[1] Noura M., Heil S., Gaedke M. (2018) GrOWTH: Goal-Oriented End User Development for Web of Things Devices. In: Mikkonen T., Klamma R., Hernández J. (eds) Web Engineering. ICWE 2018. Lecture Notes in Computer Science, vol 10845. Springer, Cham

[2] Noura M., Heil S., Gaedke M. (2019) Webifying Heterogenous Internet of Things Devices. In: Bakaev M., Frasincar F., Ko IY. (eds) Web Engineering. ICWE 2019. Lecture Notes in Computer Science, vol 11496. Springer, Cham
