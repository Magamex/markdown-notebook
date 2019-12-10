markdown-notebook
=================

Simple Android application for reading and editing markdown files 

App also may run in PC as python-kivy application

## Features

Select markdown notebook (folder)

![Image](https://i.imgur.com/8sV9tPL.png)

Select the file to open

![Image](https://i.imgur.com/gJfvSTH.png)

Select part of the file to open

![Image](https://i.imgur.com/5pYF47S.png)

Part of the file display

![Image](https://i.imgur.com/1hGGTnB.png)

Part of the file editing

![Image](https://i.imgur.com/jTXLHPV.png)

## Build and run

### PC

```bash
pip install -r requirements.txt
python3 main.py
```

### Android

#### Simple way

Upload ready [APK file](https://github.com/phpusr/markdown-notebook/releases) to phone and install it

Add permission to open files 

![Image](https://lh3.googleusercontent.com/lF7oS_cWXJAmfWy8j0JQLziTj9YySO0fHyFtyL51JSWl2iv-W0c78bsnxYezT6Iepu2bTUEpTI1G8IVDLV0l6wPQ9yFn6BwT7VhQkUZu0yYxrXW5dGkoJf4NG-v6QzLOD88QrRXtMfjx1Y4D33znO9qxvg1qAkAKbon72Kgb1190x7cPZGYNJOsaB05-WpfvlaHgYnVFPxeQXopG83Ma0gFlqhOWyvnPEI-T1fm3w_pw6fvrJG1OzrJ5aPdaM6psPFv-NGmiEMFpAnL7RGrkQ9Zkc-aOWK-mOm4ZUvFniWatPC0wh1AVOEttAd910V-sdv7efY0oP218JkUoa0N6P_Q9DqVhPsoCMAikH4ADwBDJRZK9CUh086RV17-0eoZctvIkOn87PRuBXbkP_WiUFRFFvUcdMYyTSWb9C7ntg3Secz5dudCtStOIpxKRgq9j1bEygR20sFfuxCAK5WC4oMcMVprWeFS92qaxfUSOum-1A9gofvvlA6HkDIkKrJP0TdF4kkBhzmgDfEDhf4EcDKO9AlrEtFWZK7JLIW-YUCeWrYlL6tIiel5NUN3NBVwDpLqWOGRzpFJcX-1AB2Oto2tGrqParQlu6MGkuP9nZ6YJ0GPRJsKSeUcc2ckvVYnFJ7p6Y3-_q0xLy_Z4vToZLsXdENFTf-Tgf_j0GEg4PsmtqAkhFfDus4o=w1080-h606-no)

#### Build using docker with buildozer

Edit paths in `buildozer.sh`

Run docker container with buildozer

```
./buildozer.sh
buildozer android debug
```

Upload building APK file `bin/markdownnotebook-*-armeabi-v7a-debug.apk` to phone and install it