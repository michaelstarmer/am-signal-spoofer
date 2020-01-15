'use strict'

/** @type {import('@adonisjs/lucid/src/Schema')} */
const Schema = use('Schema')

class SignalSchema extends Schema {
  up () {
    this.create('signals', (table) => {
      table.increments()
      table.string('title', 80)
      table.string('export_path', 150)
      table.string('signature_path', 150)
      table.timestamps()
    })
  }

  down () {
    this.drop('signals')
  }
}

module.exports = SignalSchema
