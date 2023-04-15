class CreateCategories < ActiveRecord::Migration[7.0]
  def change
    create_table :categories do |t|
      t.references :account, null: false
      t.bigint :parent_id
      t.text :title, null: false
      t.integer :position, null: false

      t.timestamps
    end

    add_foreign_key :categories, :accounts
  end
end
