/**
 * Helper for AccountTrigger. Creates one Opportunity per inserted Account.
 */
public with sharing class AccountTriggerHelper {

    @TestVisible
    private static final String DEFAULT_STAGE = 'Prospecting';
    @TestVisible
    private static final Integer CLOSE_DATE_DAYS = 30;

    public static void createOpportunities(List<Account> accounts) {
        List<Opportunity> opportunities = new List<Opportunity>();
        for (Account acc : accounts) {
            opportunities.add(new Opportunity(
                Name = (acc.Name + ' - Opportunity').left(120),
                AccountId = acc.Id,
                StageName = DEFAULT_STAGE,
                CloseDate = Date.today().addDays(CLOSE_DATE_DAYS)
            ));
        }
        if (!opportunities.isEmpty()) {
            insert opportunities;
        }
    }
}
