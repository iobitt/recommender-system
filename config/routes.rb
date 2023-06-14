Rails.application.routes.draw do
  resources :accounts do
    member do
      post :start_train
    end
  end

  resources :order_lines
  resources :orders
  resources :variants
  resources :products
  resources :categories
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Defines the root path route ("/")
  # root "articles#index"
  resources :installations, only: [] do
    collection do
      get :install
      get :enter
    end
  end
end
