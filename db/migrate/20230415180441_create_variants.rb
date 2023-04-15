class CreateVariants < ActiveRecord::Migration[7.0]
  def change
    create_table :variants do |t|
      t.references :account, null: false
      t.references :product, null: false
      t.text :title

      t.timestamps
    end

    add_foreign_key :variants, :accounts
    add_foreign_key :variants, :products
  end
end
