<div align="center" id="top"> 
  <img src="https://user-images.githubusercontent.com/50118124/130684955-c0ffd8f8-f8b8-4173-aae3-c3896474055f.png" alt="Pros Grafana Lib" />

  &#xa0;
</div>

<h1 align="center">PROS Grafana CLI</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/BWHS-Robotics/pros-grafana-cli?color=56BEB8">

  <!-- <img alt="Github issues" src="https://img.shields.io/github/issues/Yerti/pros-grafana-lib?color=56BEB8" /> -->

  <!-- <img alt="Github forks" src="https://img.shields.io/github/forks/Yerti/pros-grafana-lib?color=56BEB8" /> -->

  <!-- <img alt="Github stars" src="https://img.shields.io/github/stars/Yerti/pros-grafana-lib?color=56BEB8" /> -->
</p>


<h4 align="center"> 
	🚧 This library is still highly experimental  🚧
</h4> 

<hr>

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-usage">Usage</a> &#xa0; | &#xa0;
  <a href="https://github.com/Yerti" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

This project aims to improve the VEX Robotics development process by allowing statistics to easily be recorded by a V5 brain and in realtime be sent to a Grafana dashboard. The PROS Grafana Library consists of three parts:
- The [PROS C++ template](https://github.com/BWHS-Robotics/pros-grafana-lib)
- The [PROS-Grafana CLI](https://github.com/BWHS-Robotics/pros-grafana-cli), adding a custom command for brain interaction (this repository)
- (Unfinished) The optional Grafana plugin allowing for custom visualization of data such as absolute positioning 

## :sparkles: Features ##

:heavy_check_mark: Easily track multiple objects at once\
:heavy_check_mark: Easy chart and visualization creation \
:heavy_check_mark: Wireless support

## :rocket: Technologies ##

The following tools were used in this project:

- [pros-cli](https://github.com/purduesigbots/pros-cli)
- [Grafana](https://grafana.com/)
- [SQLite](https://www.sqlite.org/index.html)

## :white_check_mark: Requirements ##

Before starting :checkered_flag:, make sure you have already followed all of the steps in the [PROS Grafana Library](https://github.com/BWHS-Robotics/pros-grafana-lib) repository.

## :checkered_flag: Starting ##

You can install the PROS Grafana CLI using the following steps:

```bash
# Clone the project to the current directory
$ git clone https://github.com/BWHS-Robotics/pros-grafana-cli

# Access
$ cd pros-grafana-cli

# Install the CLI as a pip package 
$ pip install -e . 

```

Whenever you want to begin recording information, use the following command __before__ you start the program:
```bash
$ prosgrafana
```

The command will also act like a PROS terminal, and will display whatever readings it receives from the brain. 

## :memo: Sending it to Grafana ##

When you use the command `prosgrafana`, any data received by the brain will automatically be written to a file labelled `guidata.sqlite`. Grafana will need to know where this is located on your computer in order to display the information. 

<br>

Ensure you have already setup a Grafana server by following the steps [here](https://grafana.com/grafana/download). Once installed, the dashboard should be able to be opened by visiting http://localhost:3000, where both the username and password are by default `admin`:

![image](https://user-images.githubusercontent.com/36551149/159810550-0ca26e1f-c0ea-4e99-8bf1-489d9693f8c8.png)

## :gear: Configuring Grafana

As Grafana does not natively support SQLite as a data source, we'll be using the [frser-sqlite-datasource](https://grafana.com/grafana/plugins/frser-sqlite-datasource/) plugin. Follow the instructions below to install it:

- Hover over the **Gear** icon on the left side of the dashboard and click **Plugins**
- In the **Search Grafana plugins** box, search for **SQLite**
- Click on the **Install** button for the plugin 

<div align="center">
  <img src="https://user-images.githubusercontent.com/36551149/159813925-8576be4e-f5c4-4541-8f33-01b2fe908be6.png" alt="Settings Navigation"/>
</div>

Now that the plugin is installed, go back to the Settings menu and instead select the **Data Sources** tab. You should see a large blue button labelled **Add data source**.

![image](https://user-images.githubusercontent.com/36551149/159814502-080a0002-41e0-4831-9b9a-0b9ffb6a02b0.png)

After pressing it, find `SQLite` and click the **Select** button. For the `Path` input box, enter the absolute path to where your `guidata.sqlite` file is located. Hitting the `Save & test` button should result in a green checkbox and the text "Data source is working." An image for reference can be seen here:

<div align="center">
  <img src="https://user-images.githubusercontent.com/36551149/159814874-486f0c01-f796-4b8c-b4e2-3b8c871566ab.png" alt="Settings Navigation"/>
</div>

Grafana should now be ready to read any data from the program and display it in whatever visualization desired. 

## ➕ Creating dashboards 

Now that you can access the robot data, you can create a new dashboard by navigating to the following option: 
![image](https://user-images.githubusercontent.com/36551149/159810778-006406a2-618a-4552-bfcb-9792b2365def.png)

This should lead you to a new page, where you can add as many panels as you want. In this example, we'll be creating a chart displaying the velocity readings of the chassis. 

- Select the **Add an empty panel** option
- In te top right, make sure the type of panel is a **Time series**
- In the **Query** tab, change the **Data source** to **SQLite**

Your page should now look something like this:![image](https://user-images.githubusercontent.com/36551149/159811334-6d12ddc4-cfcb-4f62-9049-f08e7e870552.png)

We can now move onto the final segment: querying the SQLite file for data. 

## :memo: Writing queries ##

As the file that stores information is `.sqlite`, queries will be using the `SQL` language in order to fetch data. A few examples can be seen below:

Fetching ALL statistics being tracked 
```sql
SELECT * from data
```

Fetching a specific value requires knowing the names for variables you gave in the C++ library. 

For example, if I named a motor Variable "Left Front Motor" and tracked "Actual Velocity", you would fetch it using this query:
```sql
SELECT time, "Left Front Motor Actual Velocity" from data
``` 

Notice how `time` also has to be included for Grafana to know when certain values occur. You can fetch as many variables as you want, however there must be a ',' character between each. 

Once you're done, you can hit the "Apply" button and rearrange the chart in any fashion.

## :sparkles: Other features offered by Grafana ## 

Charts are just a tiny portion of what Grafana can do with data. You can find a list of the available visualizations [here](https://grafana.com/docs/grafana/latest/visualizations/).

<hr>

Made with :heart: by <a href="https://github.com/UZ9" target="_blank">Ryder</a>

&#xa0;

<a href="#top">Back to top</a>
