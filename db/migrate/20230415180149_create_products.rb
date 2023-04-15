class CreateProducts < ActiveRecord::Migration[7.0]
  def change
    create_table :products do |t|
      t.references :account, null: false
      t.integer :category_id, null: false
      t.text :title, null: false

      t.timestamps
    end

    add_foreign_key :products, :accounts
  end
end
