Documentation

--------------------------------------------------
--------------------------------------------------

How to setup:

	Open cmd in the main project folder and run

	python -m venv ./venv
	.\venv\Scrupts\activate
	pip install -r requirements.txt
	deactivate

	Run lagersystem.sql either in the MySQL workbench or directly in cmd
	Note that it should probably run with root permissions as I have designed the database with a root user as the highest permissions

How to run:

	Open cmd in the main project folder and run

	.\venv\Scrupts\activate
	python -m src.main
	deactivate

	Note that the user with the lowest privileges that can currently run the entire system is
	hebo_admin_schema - test123

--------------------------------------------------
--------------------------------------------------

Database design:

	The database tables were simply constructed around having the fields suggested in the assigment.
	Where Item has a foreign key on Category and Transaction has a foreign key on Item.
	I let the Primary keys for all of the table be auto incremented integers to ensure no confusion of key values.
	All dates are auto filled with the current time, to ensure that transactions and log items are counted for when the database registers them.

Database normalization:

	All tables only have one functional dependency each.
	Primary key -> {All other columns}

	This means that all of the tables are trivially in Boyce-Codd Normal Form.

	I could have created relationship tables for the connections between Item - Category and Transaction - Item, but it would be a waste of space and database actions because both relations are many to 1.

Procedures:
	
	I have placed the functionality for adding data to the tables in stored procedures, thus ensuring that I can grant a specific way of inserting without 

	I have created stored procedures for the different kinds of searches
	All tables have a generic search procedure that constructs the query to only search for the non null input parameters. To enable this I have created a stored procedure for only assigning the non null parameters to surrogate parameters. Thus enabling me to run it as a prepared statement  
	Item and Category additionally have a search procedure for finding entries with null values. These procedures are straitforwardly constructed with 'OR param IS NULL'
	Item has a procedure for finding entries with low stock. It has the optional argument for category ID, if it is NULL then it finds all entries regardles of category ID


Triggers:
	
	I have created a trigger for updating the Item stock when a Transaction is added, thus ensuring that the Item stock is kept up to date.

	I have created triggers for all operations on Item, Category and Transaction which creates a log entry containing the operation, table name, username and time when actions are performed.


Users:
	
	I have defined two levels of users
	Regular user can use stored procedures for simple reports, searches, item additions and creating Transactions.
	Super user can also use the advanced procedures as well as updating Items.

	I have defined 3 levels of admin users
	Only the first level is needed for the accessing the rest of the procedures and manipulating the rest of the tables.
	However the system doesn't have functionality for updating or removing Transactions and Logs. Additionally can't Logs can't be created manually in the system.- 

--------------------------------------------------
--------------------------------------------------

Program design:

General design:
	
	The general structure of the system is a layered architecture, with a UI, Logic and Data layer.
	It borrows some MVC controller structure, where I have made a code representation of the table rows resonsible for manupulating them.
	The Logic and Data layer both have a facade class serving as an interface where all incoming communication goes through, the only exception is the exposed properties on the model classes where the logic layer is allowed to read them.
	The UI however has a strict seperation where it only uses the logic facade (besides the __str__ overwrite of the model classes).

    I have placed a series of enum classes outside of the layered structure for comman access, for allowing actions types to be determined later in the system.
    This allowed me to consolidate functionality into fewer functions, f.x. search(SearchTypes.ITEM) and add(ObjectTyppes.ITEM) where the specific search and add functionality is later determined by this enum. 

Data layer:

    The model classes that correspond to the database tables have a common interface where they all have CRUD and get_fields functions. 
    There is technically child classes of Item based on what category the item belongs to, but I have found no extra functionality to place in the child classes.
    
    The DataConnection class is implemented as a singleton via a class decorator to ensure that there is only ever one database connection in the system.
    The DataConnection class is only responsible for taking commands and procedures and executing them. It have no knowledge of what commands, procedures and values are being executed, those are provided by the model classes or the inventory class.
    It removes all trivial packaging of results. Before returning the results it unpacks them until it encounters a datastructure with more than one value.

    The Inventory class is responsible for performing searches and using the ObjectFactory to create data objects from the results.
    It uses a factory like pattern for the different kind of searches, it contains a dict with the name of the search procedure, the search arguments and the expected object type of the results.
    It fetches the correct search function based on the value of the recieved SearchTypes enum, and thus the search function does not need to know what procedure and arguments it executes or what object type it recieves.  
    It also have the ability to return the search parameters based on SearchTypes, thus ensuring that it can inform callers of the expected input.
    The dictionary containing all the relevant info for a search means that new searches can can be added and replaced during runtime
        
    The data layer have an ObjectFactory class for instantiating all data objects. 
    It uses a dictionary for registering builders and selects them based on the ObjectTypes enum.
    Since the only required interface for the builders are build(**kwargs) then I can register other factories as builders.
    For the Item class I added the ItemFactory following the same same structure as ObjectFactory, this enables the different child classes of Item to be constructed based on the category.
    Like the Inventory class the builders can be updated and replaced during runtime.

Logic layer:

    The logic layer is largely devoid of functionality. 
    It currently only have 3 responsibilities: 
        To act as a transit between the UI and Data layer. 
        To ensure that transactions are only created if the stock is high enough.
        To generate reports.

    Like with the Inventory class i have used a factory like pattern for the ReportGenerator.
    It can return the needed parameters for generating a specific report type based on the ReportTypes enum, thus ensuring that it can inform callers of the expected input.
    It uses a factory like pattern for the different kind of reports, it contains a dict with the name of the report function and the needed arguments.
    It fetches the correct report function based on the value of the recieved ReportTypes enum, and thus the generate function does not need to know the specific function and arguments to generate a report.
    The dictionary containing all the relevant info for generating a report means that new report generators can can be added and replaced during runtime

UI layer:
    
    The UI layer consists of a series of menu classes that are instantiated and run when the user needs to be presented with a new screen.
    This enables me to have each menu have its own state and being able to remember it when returning to it from a submenu.

    I have create the general menu class UIMenu. It contains general implementations for displaying a screen, resetting a menu, running a menu and returning to a previous menu. All other menu classes inherit UIMenu thus enabling a degree of polymorphism during runtime.

    It functions by printing a list of options a user can select and a corresping dict containing the options and a corresponding function / submenu to run.

    It contains empty fields for return values, items to be displayed, status message and fields. The options and functions comes prefilled with the return function to ensure that the user can return to the previous menu unless they are explicitly overwritten.

    The return value field allows for getting information back from a submenu, and since it is defined in the UIMenu it only needs to be set at any place in the menu.

    The SearchMenu, AddMenu and UpdateMenu are general implementations for all the object and search types. When they are instantiated they recieve an enum specifying their type. 
    They then request the object or search fields from the logic facade and dynamically add options for each field and functions functions for updating them. These functions are created by having  _set_field_function setting the field and return a function for updating that field.

    This dynamic setup means that the menus will automatically change if the search parameters or object parameters change, thus decoupling it from the rest of the system to a significant degree. 
    The only real coupling between the UI and the rest of the system is that it needs to know the functions of the logic facade and what functions it is allowed to call at different points in the code.

Misc:
    
    The factory like patters allows for expanding the functionality without really affecting the other parts of the code.
    Adding new searches, reports and objects should be fairly straightforward.
    The dynamic nature of the UI means that only minor changes to it should be needed with the above kinds of changes.
    Unfortunately the logic layer needs to have some sort of coded knowlegde of the fields, because it doesn't take a user input to select the correct fields for values.

--------------------------------------------------
--------------------------------------------------

Future options:

    I could have implemented a generic DataObject defining CRUD and get_fields functions, and then have the other classes inherit it.

    Making a better search for null values where it can take non null parameters that are required to match.

    Have the logic layer translate the fields that the UI sees to the actual fields in the data layer, thus allowing for a prettier representation in the UI.
	
    I toyed with the thought of using a dict containing functions on the facades, this enabling dynamic control of the possible functions that could be called.
    
    A user table to enable control of access at the logic facade instead of denying a user access when reaching the database.    
    A function decorator for authenticating a user on the logic facade funtions.
    Have functions in the Logic layer for controlling what menu options are available based on user permissions.

    Adding various report types.
    
--------------------------------------------------
--------------------------------------------------

Notes:
	
    The class diagram is in png format instead of pdf, because drawio failed in exporting to PDF

	Using negative amount values for sales and positive values for buying couses confusion, because there is an implied sign already by the use of categories such as 'sale' and 'buy'.
	This causes a double use of sign when reading and writing the values, this negating the original sign.

    I got bitten by generalizing the UI menus and making them able to be setup dynamically, and this meant I spent an extra 8 hours on the exercise because I got a bit obsessed with seeing how far I could push it.

