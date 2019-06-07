# Template for automatically deploying python scripts and applications to Heroku Cloud

You can deploy and run almost any python application with any dependencies.

## Getting Started

1. Download or clone this repository
2. Install the python module pipreqs:

   pip install pipreqs or clone this repo @https://github.com/bndr/pipreqs.git

2. Register on [Heroku](https://www.heroku.com/)
3. Download and install [Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)
4. Download and install [git](https://git-scm.com/downloads)
5. Copy your script or project and all dependencies to this repository's folder
9. Open terminal in this directory and run hero_deploy.py


   To deploy a new heroku application to the cloud:

      ```bash
      python3 heroku_deploy.py app_name app_type main_exe
      ```

   To update an already deployed heroku application after revisions:

      ```bash
      python3 heroku_deploy.py update
      ```

   To automatically configure the dynos and launch your app, after its
   been deployed, add the optional -startapp argument.

    ```bash
    python3 heroku_deploy.py update -startapp
    ```

### Dependencies

* [pipreqs](https://github.com/bndr/pipreqs.git)

## Author

* @le-prometheen - https://thepromethean.net/
