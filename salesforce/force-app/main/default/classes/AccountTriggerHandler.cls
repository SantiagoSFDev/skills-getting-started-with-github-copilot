/**
 * Handler for AccountTrigger. Delegates business logic to AccountTriggerHelper.
 */
public with sharing class AccountTriggerHandler {

    public static void handleAfterInsert(List<Account> newAccounts) {
        AccountTriggerHelper.createOpportunities(newAccounts);
    }
}
