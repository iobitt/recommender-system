class CreateAccounts < ActiveRecord::Migration[7.0]
  def change
    create_table :accounts do |t|
      t.bigint :external_id
      t.text :shop
      t.text :token

      t.timestamps
    end
  end
end
