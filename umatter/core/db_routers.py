import random


class AppRouter:
    route_app_labels = {
        "admin": "app_db",
        "auth": "app_db",
        "sessions": "app_db",
        "contenttypes": "app_db",
        "event": "app_db",
        "friend": "app_db",
        "user": "app_db",
        "nlp": "nlp_db",
    }

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels.keys():
            return self.route_app_labels[model._meta.app_label]
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels.keys():
            return self.route_app_labels[model._meta.app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels.keys()
            or obj2._meta.app_label in self.route_app_labels.keys()
        ) and (obj1._meta.app_label == obj2._meta.app_label):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == self.route_app_labels[app_label]
        return None


class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        return random.choice(["replica",])

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        return "app_db"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        db_set = {"app_db", "replica"}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True
