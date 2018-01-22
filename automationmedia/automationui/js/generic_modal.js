var Dialog = {}

Dialog.controller = function() {
  var self = this
  self.noopContentProvider = {
    header: function() {},
    body: function() {},
    footer: function() {}
  }
  self.dialogContentProvider = self.noopContentProvider

  self.visible = m.prop(false)

  self.onclose = function() {
    self.visible(false)
    self.dialogContentProvider.onclose()
    self.dialogContentProvider = self.noopContentProvider
  }

  self.onopen = function(dialogContentProvider) {
    self.dialogContentProvider = dialogContentProvider
    self.visible(true)
  }

  radio('dialog-open').subscribe(self.onopen)
  radio('dialog-close').subscribe(self.onclose)

  self.documentHeight = function() {
    var doc = document.documentElement
    return Math.max(doc.clientHeight, window.innerHeight || 0)
  }
}

Dialog.view = function(ctrl) {
  var smallClose = m('span',
                     {onclick: ctrl.onclose},
                     m.trust('&times;'))

  var header = m('.modal-header', [
    m('button[type=button].close', [smallClose]),
    m('h4.modal-title', ctrl.dialogContentProvider.header())
  ])

  var body = m('.modal-body', [
    m('p', ctrl.dialogContentProvider.body())
  ])

  var footer = m('.modal-footer', [
    m('button[type=button].btn.btn-default',
      {onclick: ctrl.onclose},
      'Cancel'),
    ctrl.dialogContentProvider.footer()
  ])

  var modalClass = ctrl.visible() ? '.show' : ''

  var dialog = m('.modal' + modalClass, [
    m('.modal-dialog', [
      m('.modal-content', [header, body, footer])
    ])
  ])

  var maybeOverlay = ''
  if (ctrl.visible()) {
    maybeOverlay = m('.modal-backdrop.fade.in',
                     {style: 'height:' + ctrl.documentHeight() + 'px'})
  }

  return m('.row', [
    maybeOverlay,
    m('.col-lg-6.col-md-12', [dialog])
  ])
}
