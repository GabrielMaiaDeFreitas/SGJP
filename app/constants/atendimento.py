"""
Constantes utilizadas pelo módulo de Atendimento.
"""

from decimal import Decimal


# ============================================================================
# Valores Fixos
# ============================================================================

VALOR_HORA_PARADA = Decimal("80.00")

VALOR_HORA_TRABALHADA = Decimal("80.00")

VALOR_PATINS = Decimal("60.00")

KM_FRANQUIA = 40


# ============================================================================
# Status Operacional
# ============================================================================

STATUS_OPERACIONAL_PENDENTE = "Incompleto"
STATUS_OPERACIONAL_COMPLETO = "Completo"

STATUS_OPERACIONAL = [
    STATUS_OPERACIONAL_PENDENTE,
    STATUS_OPERACIONAL_COMPLETO
]

STATUS_OPERACIONAL_PADRAO = STATUS_OPERACIONAL_PENDENTE


# ============================================================================
# Status Financeiro
# ============================================================================

STATUS_FINANCEIRO_AGUARDANDO_FECHAMENTO = "Aguardando Fechamento"

STATUS_FINANCEIRO_AGUARDANDO_PAGAMENTO = "Aguardando Pagamento"

STATUS_FINANCEIRO_PAGAMENTO_PARCIAL = "Pagamento Parcial"

STATUS_FINANCEIRO_PAGO = "Pago"

STATUS_FINANCEIRO = [
    STATUS_FINANCEIRO_AGUARDANDO_FECHAMENTO,
    STATUS_FINANCEIRO_AGUARDANDO_PAGAMENTO,
    STATUS_FINANCEIRO_PAGAMENTO_PARCIAL,
    STATUS_FINANCEIRO_PAGO
]

STATUS_FINANCEIRO_PADRAO = STATUS_FINANCEIRO_AGUARDANDO_FECHAMENTO