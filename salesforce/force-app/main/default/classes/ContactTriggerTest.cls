@IsTest
private class ContactTriggerTest {

    @IsTest
    static void createsOneOpportunityPerContact() {
        Account acc = new Account(Name = 'Contact Parent Account');
        insert acc;
        // Discard the Opportunity created by AccountTrigger so only Contact Opportunities are counted
        delete [SELECT Id FROM Opportunity WHERE AccountId = :acc.Id];

        List<Contact> contacts = new List<Contact>();
        for (Integer i = 0; i < 200; i++) {
            contacts.add(new Contact(FirstName = 'Test', LastName = 'Contact ' + i, AccountId = acc.Id));
        }

        Test.startTest();
        insert contacts;
        Test.stopTest();

        List<Opportunity> opps = [
            SELECT Id, Name, AccountId, StageName, CloseDate
            FROM Opportunity
            WHERE AccountId = :acc.Id
        ];
        System.assertEquals(contacts.size(), opps.size(), 'One Opportunity per Contact expected');
        for (Opportunity opp : opps) {
            System.assert(opp.Name.startsWith('Test Contact '), 'Opportunity name should use the Contact name');
            System.assertEquals(ContactTriggerHelper.DEFAULT_STAGE, opp.StageName);
            System.assertEquals(Date.today().addDays(ContactTriggerHelper.CLOSE_DATE_DAYS), opp.CloseDate);
        }
    }

    @IsTest
    static void createsOpportunityForContactWithoutAccount() {
        Contact con = new Contact(LastName = 'Orphan');

        Test.startTest();
        insert con;
        Test.stopTest();

        List<Opportunity> opps = [SELECT Id, Name, AccountId FROM Opportunity WHERE Name = 'Orphan - Opportunity'];
        System.assertEquals(1, opps.size(), 'One Opportunity expected for the Contact');
        System.assertEquals(null, opps[0].AccountId);
    }
}
