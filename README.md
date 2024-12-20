# hs_workflow_find_contact_from_website
The custom code in HubSpot workflow will fetch an email from a website to create a contact in CRM.

## Automatically creates a Contact from your customer's website
HubSpot CRM can enrich Contacts' data with Company information but not the other direction. Sometime we would like to reachout customer from their website where email is avaliable.
Powered by HubSpot workflow, when a company record is created, this custom Python code fetch an email from the website, for the workflow to create contact.

## Workflow
<img width="379" alt="Screenshot 2024-12-08 at 2 23 39 PM" src="https://github.com/user-attachments/assets/660242f3-5187-4c41-af53-2a6b9268512c">

## Install steps and DEMO
[Loom Video](https://www.loom.com/share/1af8529374b043199e34828b456fb92d?sid=fe4d5bd2-b4f2-4365-85d7-f4474a8178ea)

## Other Technical Details
* Class LinkParser is to replace BeautifulSoup since it is not supported in HubSpot workflow Python custom code :(
* Email link from popular website hosting service is filtered(ex: wixpress.com, godaddy.com, mysite.com, etc.)
