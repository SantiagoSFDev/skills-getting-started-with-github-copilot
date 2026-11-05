trigger ContactTrigger on Contact (after insert) {
    ContactTriggerHandler.handleAfterInsert(Trigger.new);
}
