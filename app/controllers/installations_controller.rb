# frozen_string_literal: true

class InstallationsController < ApplicationController
  def install
    ExtraLogger.info('New installation', self.class, **permitted_params)
    Account.create!(permitted_params)
    head :ok
  end

  private

  def permitted_params
    params.permit(:shop, :insales_id, :token).tap { _1[:external_id] = _1.delete(:insales_id) }
  end
end
