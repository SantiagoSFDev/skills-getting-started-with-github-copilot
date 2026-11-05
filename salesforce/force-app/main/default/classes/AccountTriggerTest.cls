@IsTest
private class AccountTriggerTest {

    @IsTest
    static void createsOneOpportunityPerAccount() {
        List<Account> accounts = new List<Account>();
        for (Integer i = 0; i < 200; i++) {
            accounts.add(new Account(Name = 'Test Account ' + i));
        }

        Test.startTest();
        insert accounts;
        Test.stopTest();

        Set<Id> accountIds = new Map<Id, Account>(accounts).keySet();
        List<Opportunity> opps = [
            SELECT Id, Name, AccountId, StageName, CloseDate
            FROM Opportunity
            WHERE AccountId IN :accountIds
        ];
        System.assertEquals(accounts.size(), opps.size(), 'One Opportunity per Account expected');

        Map<Id, Integer> countByAccount = new Map<Id, Integer>();
        for (Opportunity opp : opps) {
            Integer current = countByAccount.containsKey(opp.AccountId) ? countByAccount.get(opp.AccountId) : 0;
            countByAccount.put(opp.AccountId, current + 1);
            System.assertEquals(AccountTriggerHelper.DEFAULT_STAGE, opp.StageName);
            System.assertEquals(Date.today().addDays(AccountTriggerHelper.CLOSE_DATE_DAYS), opp.CloseDate);
        }
        for (Id accId : accountIds) {
            System.assertEquals(1, countByAccount.get(accId), 'Each Account should have exactly one Opportunity');
        }
    }
}
