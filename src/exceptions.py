class LivreIndisponibleError(Exception):
    def __init__(self, message="ce livre n'est pas disponible."):
        super().__init__(message)

class QuotaEmpruntDepasseError(Exception):
    def __init__(self, message=" le membre a déjà emprunté le nombre maximum de livres autorisés."):
        super().__init__(message)

class MembreInexistantError(Exception):
    def __init__(self, message="ce membre n'est pas inscrit dans la bibliotheque."):
        super().__init__(message)

class LivreInexistantError(Exception):
    def __init__(self, message="ce livre n'existe pas dans la bibliotheque."):
        super().__init__(message)