class CreateOrders < ActiveRecord::Migration[7.0]
  def change
    create_table :orders do |t|
      t.references :account, null: false
      t.bigint :client_id, null: false
      t.decimal :total_price, null: false

      t.timestamps
    end

    add_foreign_key :variants, :accounts
  end
end
