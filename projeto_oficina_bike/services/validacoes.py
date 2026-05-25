def campo_vazio(*campos):
    """Retorna True se algum campo estiver vazio."""
    for campo in campos:
        if not campo or str(campo).strip() == "":
            return True
    return False

def senhas_iguais(senha, confirmar):
    """Verifica se as senhas são iguais."""
    return senha == confirmar

def email_valido(email):
    """Verifica se o e-mail contém @ e ponto."""
    return "@" in email and "." in email

def valor_valido(valor):
    """Verifica se o valor é numérico e positivo."""
    try:
        v = float(valor.replace(",", "."))
        return v >= 0
    except (ValueError, AttributeError):
        return False
