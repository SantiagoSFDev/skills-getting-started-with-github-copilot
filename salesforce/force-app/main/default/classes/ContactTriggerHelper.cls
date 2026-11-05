/**
 * Helper for ContactTrigger. Creates one Opportunity per inserted Contact.
 */
public with sharing class ContactTriggerHelper {

    @TestVisible
    private static final String DEFAULT_STAGE = 'Prospecting';
    @TestVisible
    private static final Integer CLOSE_DATE_DAYS = 30;

    public static void createOpportunities(List<Contact> contacts) {
        List<Opportunity> opportunities = new List<Opportunity>();
        for (Contact con : contacts) {
            String contactName = String.isBlank(con.FirstName)
                ? con.LastName
                : con.FirstName + ' ' + con.LastName;
            opportunities.add(new Opportunity(
                Name = (contactName + ' - Opportunity').left(120),
                AccountId = con.AccountId,
                StageName = DEFAULT_STAGE,
                CloseDate = Date.today().addDays(CLOSE_DATE_DAYS)
            ));
        }
        if (!opportunities.isEmpty()) {
            insert opportunities;
        }
    }
}
