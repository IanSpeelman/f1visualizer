# F1Visualizer

#### video demo https://youtu.be/wEHUQEHRBeo
#### Description

**F1Visualizer** is a comprehensive platform designed to visualize statistics in Formula One. Built to enhance the experience of F1 enthusiasts, this website offers a robust set of features for comparing drivers, checking session results, and managing race events. Here’s a detailed look at what F1Visualizer provides:

### Key Features

#### 1. Compare Drivers

One of the standout features of F1Visualizer is its ability to compare drivers' performances throughout the season. Users can:

-  **Select Multiple Drivers**: Choose from a list of drivers to compare their performance metrics.
-  **Performance Visualization**: View intuitive line graphs that display the comparative performance of selected drivers over various races.
-  **Dynamic Data Fetching**: After selecting a driver, the relevant data is fetched from the frontend without requiring a page reload, ensuring a seamless user experience.

This feature is particularly useful for fans and analysts who want to track driver progress, identify trends, and make data-driven comparisons.

#### 2. Check Session Results

The Results page is designed to provide detailed information about race results. It includes:

-  **Comprehensive Table View**: Browse through a table that displays all uploaded race results.

By presenting race results in an organized and accessible manner, users can quickly access the information they need without hassle.

#### 3. Create New Events

Creating new events in F1Visualizer is straightforward and customizable. Users can:

-  **Specify Session Start Times**: Input start times for all five sessions that typically occur during a Formula One weekend.
-  **Sprint Weekend Customization**: Modify the weekend structure to accommodate sprint weekends, which have a different format than regular race weekends.
-  **Event Integration**: Once created, the event will appear as an option in the "Upload Results" section.

This feature allows users to tailor the event setup to match the specific requirements of each race weekend, ensuring flexibility and accuracy in event management.

#### 4. Upload Results

Uploading race results is a critical function of F1Visualizer. The process includes:

-  **Event and Session Selection**: Users must select an event and a specific session (e.g., practice, qualifying, race) for which they want to upload results.
-  **Document Upload**: Upload session classification documents and entry lists that are published by the FIA.
-  **Data Extraction and Confirmation**: Utilizing `camelot-py`, the system extracts information from the PDF files and prompts the user to confirm its accuracy. This step ensures that the data is correctly interpreted before being stored in the database.
-  **Database Storage**: Once confirmed, the data is uploaded to the database, making it available for future reference and analysis.

**Note**: `camelot-py` requires Ghostscript to be installed. Instructions for installing Ghostscript can be found in the [Camelot documentation](https://camelot-py.readthedocs.io/en/master/user/install-deps.html).

**example document**: the documents to be uploaded look like [this one](https://i.imgur.com/MnDSJE2.jpeg)

By streamlining the data upload process, F1Visualizer ensures that users can efficiently manage and update race results.

#### 5. View Results

The Results page is a central hub for accessing uploaded race data. Features include:

-  **Dynamic Loading**: Results are fetched dynamically from the database and displayed without requiring a page reload, providing a smooth and responsive user experience.
-  **Event and Session Filtering**: Users can easily see which events and sessions have results uploaded, making navigation straightforward.

This dynamic approach ensures that users always have access to the most up-to-date information in a user-friendly format.

### Technologies Used

F1Visualizer leverages a robust technology stack to deliver its features:

-  **Backend**: The backend is powered by Python and Flask, providing a reliable and scalable foundation for handling data and user requests.
-  **Frontend**: The frontend is built with HTML, CSS, and JavaScript, ensuring a responsive and interactive user interface.
-  **PDF Data Extraction**: `camelot-py` is used to extract data from PDF documents, automating the process of data entry and minimizing errors.
-  **Data Visualization**: `Chart.js` is employed to render interactive and visually appealing charts for driver comparisons and other visual data representations.
-  **Database**: `SQLite3` is used for efficient and reliable data storage.

By integrating these technologies, F1Visualizer offers a seamless, efficient, and enjoyable experience for users looking to explore and analyze Formula One data.

### Conclusion

F1Visualizer is more than just a website; it’s a comprehensive tool designed for Formula One enthusiasts, analysts, and professionals. With its robust features for comparing drivers, checking session results, creating events, and uploading data, it stands as an essential resource for anyone looking to delve deeper into the world of Formula One statistics. Whether you’re a fan wanting to compare your favorite drivers or an analyst looking for detailed race data, F1Visualizer provides the tools and functionalities to meet your needs.
