class CreateOrderLines < ActiveRecord::Migration[7.0]
  def change
    create_table :order_lines do |t|
      t.references :account, null: false
      t.references :order, null: false
      t.references :product, null: false
      t.references :variant, null: false
      t.text :title, null: false
      t.integer :quantity, null: false

      t.timestamps
    end

    add_foreign_key :order_lines, :accounts
    add_foreign_key :order_lines, :orders
    add_foreign_key :order_lines, :products
    add_foreign_key :order_lines, :variants
  end
end
