

class AddJobOpeningLocators:
   Job_opening_side_button = "a[href='#/dashboard/jobopening']"
   Add_job_opening_button = "//button[@class='jo-screen-new__add-btn']"
   Full_setup_button = "//button[.//h3[normalize-space()='Full Setup']]"
   Continue_button = "//button[text()='Continue']"

   # fill the form of job opening

   # Upload the resume of the candidate
   Click_Upload_JD = "//button[@class='MuiBox-root css-yeps5k']"
   # Click on browser file text
   Click_Browser_File_Text = "//input[@type='file']"
   Generate_From_JD_Button = "//button[normalize-space()='Generate from JD']"

   # Enter job title
   Add_job_title = "//input[@placeholder='Type or select a role…']"

   # click on the + icon to add the job title
   Click_job_title_plus_icon = "div.MuiPopover-root:visible [data-testid='AddIcon']"

   # Add education
   Add_Education = "//input[@placeholder='e.g. B.Tech / B.E.']"
   Add_Department = "//input[@placeholder='Select or Enter Department']"
   Add_Industry = "//input[@placeholder='Select or Enter Industry / Domain']"
   Add_Seniority_level = "//span[normalize-space()='Seniority level *']/following::div[@role='combobox'][1]"
   Add_Experience_Min = "(//input[@placeholder='Min'])[1]"
   Add_Experience_Max = "(//input[@placeholder='Max'])[1]"
   Add_Salary_Min = "(//input[@placeholder='Min'])[2]"
   Add_Salary_Max = "(//input[@placeholder='Max'])[2]"
   Add_Job_Content = "(//div[contains(@class,'jodit-wysiwyg') and @contenteditable='true'])[1]"
   Add_Key_responsibilities = "(//div[contains(@class,'jodit-wysiwyg') and @contenteditable='true'])[2]"

   # Add skills
   Add_Skills = "//input[@placeholder='Add required skill, press Enter...']"

   # Add locations
   Add_location = "//input[@placeholder='e.g. Bengaluru, Remote...']"

   Work_Mode_Onsite = "//button[normalize-space()='Onsite']"
   Employment_Type_Full_Time = "//button[normalize-space()='Full Time']"
   Number_Of_Openings = "//input[@type='number']"

   # 2nd screen

   # add team lead
   Add_TeamLead = "//*[contains(normalize-space(), 'Select Team Lead...') and not(*)]"

   # Add recruiter
   Add_Recruiter = "//*[normalize-space()='Select recruiters...' and not(*)]"

   # Add BU
   Add_BU = "//input[@placeholder='Enter business unit...']"

   # Add close date
   Target_Closure_Date = "input[type='date']"

   # Select Urgent
   Select_Urgent = "//span[normalize-space()='Urgent']"

   # Select Workflow Stages
   Select_Technical_round = "//button[normalize-space()='Technical Round']"
   Select_HR_Round = "//button[normalize-space()='HR Round']"
   Select_Managerial_Round = "//button[normalize-space()='Managerial Round']"

   # click on the generate button
   Click_AIGenerate_Button = "//button[text()='Generate']"

   # Back and Save as Draft buttons
   Back_Button = "//button[normalize-space()='Back']"
   Save_As_Draft_Button = "//button[normalize-space()='Save as Draft']"

   # click on Add job opening button
   Click_Add_Job_Opening_Button_f = "//button[text()='Add Job Opening']"

   # Search the job opening to verify
   Search_JobOpening = "//input[@placeholder='Search by title, department or location']"

   # Verify the ACTIVE status on the newly created Job opening
   Active_status = "//span[@class='jo-card-new__status jo-card-new__status--active']"

   # ensure active tab is clicked
   Active_tab = "//button[contains(normalize-space(),'Active')]"
   Inactive_tab = "//button[contains(normalize-space(),'Inactive')]"

   # save the id
   JO_id = "//p[contains(@class,'jo-card-new__job-id')]"

   # check the checkbox
   JO_checkbox = "//input[@type='checkbox']"

   # click on the inactive button
   INACTIVE_BUTTON = "//button[normalize-space()='Inactive']"

   # now verify the JO id in Inactive screen
   Inactive_Job_Id = "//p[contains(@class,'jo-card-new__job-id')]"

   # success toaster / notification message
   Inactive_Success_Message = "//div[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'job opening got inactive')]"

   #Validate the the counter of number of openings
   COUNTER_NUMBEROFOPENING = "//span[@class='jo-card-new__openings-pill']"

   # Job opening cards are rendered as article elements in the Job Openings list.
   JOB_OPENING_CARD = "article"
