/**
 * Handler for ContactTrigger. Delegates business logic to ContactTriggerHelper.
 */
public with sharing class ContactTriggerHandler {

    public static void handleAfterInsert(List<Contact> newContacts) {
        ContactTriggerHelper.createOpportunities(newContacts);
    }
}
