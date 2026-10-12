// Exercise the exact inbox implementation from the collected bundle in isolation.
// Protocol constructors are stubbed; no Bot, model, tool or remote service is run.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');

const bundle = fs.readFileSync(path.join(__dirname,
  '../sources/opt/sand/sand-host/sand-eval-runner.cjs'), 'utf8');
const marker = '// ../packages/grok-bot-harness/src/runner/steer/turn-steer.ts';
const start = bundle.indexOf(marker);
assert(start >= 0, 'Inbox module must exist in the collected bundle');
const end = bundle.indexOf('\n// ', start + marker.length);
assert(end > start, 'Inbox module boundary must exist');

class ProtocolMessage {
  constructor(fields) { Object.assign(this, fields); }
}
const context = {
  UserMessage: ProtocolMessage,
  UserMessageAction: ProtocolMessage,
  ConversationAction: ProtocolMessage,
  crypto,
  hiddenPromptMarker: () => '[hidden]',
  SAND_OFF_RECORD_MESSAGE_ID_PREFIX: 'probe:',
  toRedactedConversationAction: action => action,
};
vm.runInNewContext(bundle.slice(start, end) +
  '\nglobalThis.Inbox = SandSteerInbox;', context);

(async () => {
  const inbox = new context.Inbox(() => false);
  assert.equal(inbox.enqueue('before run', {}).kind, 'no-live-run');
  inbox.beginRun();
  const receiver = inbox.receiver('probe');
  let admissions = 0;
  const unsubscribe = receiver.getContextInjectionToolSignal()
    .onUserInjectionAdmitted(() => admissions++);
  const first = inbox.enqueue('first', {});
  const second = inbox.enqueue('second', {});
  assert.equal(admissions, 2);
  assert.equal((await receiver.peek()).action.value.userMessage.text, 'first');
  assert.equal((await receiver.pop()).action.value.userMessage.text, 'first');
  assert.equal(receiver.failConsumedInjectionDelivery(), true);
  assert.equal((await receiver.peek()).action.value.userMessage.text, 'first');
  await receiver.pop();
  assert.equal((await receiver.peek()).action.value.userMessage.text, 'second');
  assert.equal(await first.deliveredAtStepBoundary, true);
  inbox.endRun();
  assert.equal(await second.deliveredAtStepBoundary, false);
  assert.equal(inbox.enqueue('after run', {}).kind, 'no-live-run');
  unsubscribe();
  console.log(JSON.stringify({
    source: 'collected SandSteerInbox implementation',
    checks: ['live-run admission', 'admission notification', 'FIFO',
      'failed-delivery requeue', 'delivery acknowledgment', 'run-end rejection'],
    result: 'passed',
    scope: 'isolated inbox; does not establish cloud Workflow behavior',
  }, null, 2));
})().catch(error => { console.error(error.message); process.exitCode = 1; });
