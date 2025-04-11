`https://fast-dds.docs.eprosima.com/en/latest/docker/docker.html`
Click `eProsima’s downloads page`, fill in contact info, select "Available Versions" under eProsima Fast DDS, click on Version 3.1.2, then scroll to and click 'Download now' for "ubuntu-fastdds v3.1.2.tar"

Save that .tar file in a directory. Open a command prompt and go to the directory where the .tar file is stored. Run `docker load -i ubuntu-fastdds-3.1.2.tar` and then `docker run -it ubuntu-fastdds:v3.1.2`. If you get a different shell prompt, it means it loaded correctly.

Open VSCode and navigate to the extension page. Install the Docker and Dev Containers extensions (both uploaded by Microsoft). Also install Docker DX as it may be helpful in the future.

You can start the docker image in 2 ways. 
1. You can install the Docker application to start your images with one button.
2. You can run the `docker run -it ubuntu-fastdds:v3.1.2` to start the image

In the bottom left of your vscode, there should be a blue button. Clicking that will open a drop down on the search bar. Click "Attach to a running container" and select
