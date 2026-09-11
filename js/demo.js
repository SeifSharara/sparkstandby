/* Deterministic, browser-only demo. No requests, storage, calls, or real SMS. */
(function () {
  'use strict';
  const workspace = document.getElementById('demo-workspace');
  if (!workspace) return;
  const byId = (id) => document.getElementById(id);
  const phone = byId('phone-shell');
  const callScreen = byId('call-screen');
  const smsScreen = byId('sms-screen');
  const messages = byId('messages');
  const choices = byId('reply-choices');
  const owner = byId('owner-panel');
  const result = byId('demo-result');
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const timers = new Set();
  let phase = 'call';
  let selectedService = null;
  let detail = '';
  let preference = '';
  let nextStep = '';
  let isTyping = false;
  const branches = {
    repair: {
      label: 'My AC isn’t cooling', service: 'AC Repair',
      handoff: 'The team can discuss availability and the right next step.',
      question: 'Is the system running but blowing warm air, or has it stopped running entirely?',
      details: [
        { label: 'Running, but blowing warm air', summary: 'System is running but blowing warm air.', nextStep: 'Call Sarah about the cooling issue' },
        { label: 'It has stopped running', summary: 'AC system has stopped running entirely.', nextStep: 'Call Sarah about the stopped system' }
      ],
      next: 'Thanks for the details. When would you like the team to follow up?',
      preferences: [
        { label: 'As soon as possible', summary: 'Customer would like service and a callback as soon as possible.', reply: 'Thanks, Sarah. I’ve shared the cooling issue and your request for a callback as soon as possible. The team will confirm availability with you.' },
        { label: 'Tomorrow works', summary: 'Customer would like service and a callback tomorrow.', reply: 'Thanks, Sarah. I’ve shared the cooling issue and your request for a callback tomorrow. The team will confirm availability with you.' }
      ]
    },
    quote: {
      label: 'I need a quote', service: 'Installation Quote',
      handoff: 'Discuss scope and timing before preparing an estimate.',
      question: 'Of course. Is this for replacing an existing system or installing one in a new space?',
      details: [
        { label: 'Replacing my current system', summary: 'Customer wants a quote to replace an existing HVAC system.', nextStep: 'Discuss a system replacement quote' },
        { label: 'An installation in a new space', summary: 'Customer wants a quote for an HVAC installation in a new space.', nextStep: 'Discuss a new installation quote' }
      ],
      next: 'Got it. Are you ready to discuss the project, or just planning ahead?',
      preferences: [
        { label: 'I’m ready to get started', summary: 'Customer is ready to discuss the project.', reply: 'Thanks, Sarah. I’ve let the team know you’d like a quote and are ready to discuss the project. They can talk through the options with you.' },
        { label: 'Just planning ahead', summary: 'Customer is planning ahead and comparing options.', reply: 'Thanks, Sarah. I’ve noted that you’re planning ahead and comparing options. The team can help you understand what the project would involve.' }
      ]
    },
    maintenance: {
      label: 'I need maintenance', service: 'HVAC Maintenance',
      handoff: 'The team can discuss the work and confirm availability.',
      question: 'Happy to help. Is this a seasonal tune-up, or is there something specific you’ve noticed?',
      details: [
        { label: 'A seasonal tune-up', summary: 'Customer is requesting a seasonal HVAC tune-up.', nextStep: 'Discuss a seasonal tune-up' },
        { label: 'It’s making an unusual noise', summary: 'Customer reports an unusual noise and wants the system checked.', nextStep: 'Discuss a system inspection' }
      ],
      next: 'Thanks. When would you like the team to follow up?',
      preferences: [
        { label: 'As soon as possible', summary: 'Customer would like a callback as soon as possible.', reply: 'Thanks, Sarah. I’ve shared your maintenance inquiry and request for a callback as soon as possible. The team will confirm the next step with you.' },
        { label: 'Sometime this week', summary: 'Customer would like a callback this week.', reply: 'Thanks, Sarah. I’ve shared your maintenance inquiry and request for a callback this week. The team will confirm the next step with you.' }
      ]
    }
  };

  function later(callback, delay) {
    const timer = window.setTimeout(() => { timers.delete(timer); callback(); }, motion.matches ? 0 : delay);
    timers.add(timer);
  }
  function announce(text) { byId('demo-announcement').textContent = text; }
  function focus(element) { element.focus({ preventScroll: true }); }
  function revealFocus(element) {
    focus(element);
    const bounds = element.getBoundingClientRect();
    if (bounds.top < 90 || bounds.bottom > window.innerHeight) {
      element.scrollIntoView({ block: 'nearest', behavior: motion.matches ? 'instant' : 'smooth' });
    }
  }
  function progress(step) {
    document.querySelectorAll('.demo-steps li').forEach((item, index) => {
      item.classList.toggle('current', index === step);
      item.classList.toggle('complete', index < step);
      if (index === step) item.setAttribute('aria-current', 'step');
      else item.removeAttribute('aria-current');
    });
  }
  function guide(title, instruction) {
    byId('demo-step-title').textContent = title;
    byId('demo-instruction').textContent = instruction;
  }
  function addMessage(text, kind) {
    const message = document.createElement('p');
    message.className = kind === 'meta' ? 'message-meta' : 'message ' + kind;
    message.textContent = text;
    if (kind !== 'meta') {
      const speaker = document.createElement('span');
      speaker.className = 'sr-only';
      speaker.textContent = kind === 'customer' ? 'Sarah: ' : 'Northline: ';
      message.prepend(speaker);
    }
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
  }
  function automatedReply(text, after) {
    choices.replaceChildren();
    isTyping = true;
    choices.setAttribute('aria-busy', 'true');
    byId('reply-label').textContent = 'NORTHLINE IS TYPING…';
    const typing = document.createElement('div');
    typing.className = 'message automated typing-indicator';
    typing.setAttribute('aria-hidden', 'true');
    for (let i = 0; i < 3; i++) typing.appendChild(document.createElement('span'));
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;
    later(() => {
      typing.remove();
      isTyping = false;
      choices.setAttribute('aria-busy', 'false');
      addMessage(text, 'automated');
      after();
      messages.scrollTop = messages.scrollHeight;
    }, 750);
  }
  function showChoices(options, onSelect) {
    choices.replaceChildren();
    const question = { service: 1, detail: 2, preference: 3 }[phase];
    byId('reply-label').textContent = 'CHOOSE SARAH’S REPLY · ' + question + ' OF 3';
    options.forEach((option) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = option.label;
      button.addEventListener('click', () => {
        if (button.disabled || isTyping) return;
        choices.querySelectorAll('button').forEach((item) => { item.disabled = true; });
        addMessage(option.label, 'customer');
        onSelect(option);
      }, { once: true });
      choices.appendChild(button);
    });
    focus(choices.firstElementChild);
  }
  function startConversation() {
    phase = 'service';
    callScreen.classList.remove('is-leaving');
    callScreen.hidden = true;
    smsScreen.hidden = false;
    phone.classList.add('is-messaging');
    progress(1);
    guide('A missed call becomes a conversation.', 'Choose Sarah’s replies below. A few helpful questions give the business a clearer picture.');
    byId('device-caption').textContent = 'You’re choosing the customer’s replies.';
    addMessage('Today · Sarah agreed to receive texts', 'meta');
    automatedReply('Hi Sarah, sorry we missed your call. This is Northline Heating & Air. How can we help? Reply STOP to opt out.', () => {
      showChoices(Object.entries(branches).map(([key, value]) => ({ key, label: value.label })), (option) => {
        selectedService = branches[option.key];
        phase = 'detail';
        automatedReply(selectedService.question, () => {
          showChoices(selectedService.details, (selection) => {
            detail = selection.summary;
            nextStep = selection.nextStep;
            phase = 'preference';
            automatedReply(selectedService.next, () => {
              showChoices(selectedService.preferences, (selection) => {
                preference = selection.summary;
                phase = 'ready';
                automatedReply(selection.reply, () => {
                  byId('reply-label').textContent = 'NOW SEE WHAT THE BUSINESS RECEIVES';
                  const reveal = document.createElement('button');
                  reveal.type = 'button';
                  reveal.className = 'reveal-button';
                  reveal.textContent = 'See the business side →';
                  reveal.addEventListener('click', revealLead, { once: true });
                  choices.appendChild(reveal);
                  focus(reveal);
                  announce('Conversation complete. Select See the business side to see the captured lead.');
                });
              });
            });
          });
        });
      });
    });
  }
  function revealLead() {
    if (phase !== 'ready' || isTyping) return;
    phase = 'handoff';
    const stage = document.querySelector('.device-stage');
    choices.querySelectorAll('button').forEach((button) => { button.disabled = true; });
    stage.classList.add('is-leaving');
    announce('Opening the business view with Sarah’s inquiry.');
    later(() => {
      phase = 'complete';
      workspace.classList.add('is-complete');
      stage.hidden = true;
      stage.classList.remove('is-leaving');
      owner.hidden = false;
      byId('lead-service').textContent = selectedService.service;
      byId('lead-summary').textContent = detail + ' ' + preference;
      byId('lead-next-step').textContent = nextStep;
      byId('lead-next-note').textContent = selectedService.handoff;
      byId('demo-perspective').textContent = 'The business experience';
      progress(2);
      guide('A useful inquiry. Ready for your callback.', 'You know why Sarah called and what she needs next. Pick up the conversation without starting from scratch.');
      const statuses = document.querySelectorAll('.workflow-statuses li');
      statuses.forEach((status, index) => {
        later(() => {
          status.classList.add('done');
          if (index === statuses.length - 1) {
            result.hidden = false;
            announce('Demo complete. Lead captured, conversation logged, and business notified. No real messages were sent.');
          }
        }, 160 + index * 150);
      });
      revealFocus(owner);
    }, 180);
  }
  function reset() {
    timers.forEach((timer) => window.clearTimeout(timer));
    timers.clear();
    phase = 'call'; selectedService = null; detail = ''; preference = ''; nextStep = ''; isTyping = false;
    workspace.classList.remove('is-complete', 'show-conversation');
    document.querySelector('.device-stage').hidden = false;
    document.querySelector('.device-stage').classList.remove('is-leaving');
    callScreen.classList.remove('is-leaving');
    byId('demo-perspective').textContent = 'The customer experience';
    owner.hidden = true; result.hidden = true; smsScreen.hidden = true; callScreen.hidden = false;
    phone.classList.remove('is-messaging', 'is-missed');
    messages.replaceChildren(); choices.replaceChildren();
    choices.setAttribute('aria-busy', 'false');
    byId('reply-label').textContent = 'CHOOSE SARAH’S REPLY';
    byId('lead-next-step').textContent = 'Call Sarah to discuss service';
    byId('lead-next-note').textContent = 'You decide availability and confirm the next step.';
    byId('lead-summary').textContent = '';
    byId('lead-service').textContent = 'AC Repair';
    document.querySelectorAll('.workflow-statuses li').forEach((item) => item.classList.remove('done'));
    byId('call-state').textContent = 'Incoming call';
    byId('miss-call').disabled = false;
    byId('miss-call').querySelector('span').textContent = 'Miss Call';
    byId('device-caption').textContent = 'Fictional customer. Real-world possibility.';
    byId('view-conversation').setAttribute('aria-expanded', 'false');
    byId('view-conversation').innerHTML = 'View the conversation <span aria-hidden="true">↗</span>';
    guide('You’re busy. A new customer is calling.', 'Sarah is calling about her home’s heating and air. You’re on another job and can’t pick up.');
    progress(0);
    announce('Demo restarted. Sarah is calling.');
    revealFocus(byId('miss-call'));
  }
  byId('miss-call').addEventListener('click', () => {
    if (phase !== 'call') return;
    phase = 'processing';
    phone.classList.add('is-missed');
    byId('miss-call').disabled = true;
    byId('miss-call').querySelector('span').textContent = 'Call missed';
    byId('call-state').textContent = 'Missed call';
    announce('Missed call detected. In this example, Sarah agrees to receive a text.');
    later(() => {
      byId('call-state').textContent = 'Sarah agrees to a text · Starting follow-up…';
      later(() => {
        callScreen.classList.add('is-leaving');
        later(startConversation, 180);
      }, 620);
    }, 650);
  });
  byId('demo-reset').addEventListener('click', reset);
  byId('demo-replay').addEventListener('click', reset);
  byId('view-conversation').addEventListener('click', () => {
    const stage = document.querySelector('.device-stage');
    stage.hidden = !stage.hidden;
    workspace.classList.toggle('show-conversation', !stage.hidden);
    byId('view-conversation').textContent = stage.hidden ? 'View the conversation' : 'Hide the conversation';
    byId('view-conversation').setAttribute('aria-expanded', String(!stage.hidden));
    if (!stage.hidden) {
      choices.replaceChildren();
      byId('reply-label').textContent = 'CONVERSATION COMPLETE';
      byId('device-caption').textContent = 'Sarah’s conversation · Read from the beginning above.';
      messages.scrollTop = messages.scrollHeight;
      revealFocus(messages);
    }
  });
})();
