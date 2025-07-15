from pydantic import BaseModel, Field, model_validator

class AuthRequest(BaseModel):
    ip: str | None = Field(None, description="IP-адрес клиента")
    reg_num: str | None = Field(None, description="Регистрационный номер клиента")

    @model_validator(mode="after")
    def check_ip_or_reg_num(self):
        if not self.ip and not self.reg_num:
            raise ValueError("Either 'ip' or 'reg_num' must be provided.")
        return self

class AuthResponse(BaseModel):
    success: bool = Field(..., description="Флаг успешности авторизации")
