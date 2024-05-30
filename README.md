# TalanaKombat

## Instrucciones:

Para ejecutar basta con entrar a /app y ejecutar `python main.py`, te todas formas agrego el makefile con los comandos run, build y d-run para correr con docker incluso si se desea, basta con llamar a `make run` o si sq quiere con docker `make build` y luego `make d-run`.

## Preguntas generales:

1. Supongamos que en un repositorio GIT hiciste un commit y olvidaste un archivo. Explica
   cómo se soluciona si hiciste push, y cómo si aún no hiciste.

   - Lo que se debe hacer en ambos casos es modificar el commit anterior, lo que implica sobreescribir el historial del commits del repositorio.
     - Para el caso que aún no haya subido el cambio con push basta con solo agregar el archivo olvidado con `git add <archivo_olvidado>` y luego enmendar o corregir el ultimo commit `git commit --amend <--no-edit>` (el --no-edit es para no modificar el mensaje del commit anterior) y finalmente puedo verificar el status con `git status`. Luego sigo como siempre con `git push` etc etc.
     - Si ya hice push hago lo mismo, agregar el archivo olvidado con `git add <archivo_olvidado>` y luego enmendar o corregir el ultimo commit `git commit --amend <--no-edit>`y puedo verificar el status con `git status`. Pero ahora tengo que forzar el cambio del historial del repositorio remoto con `git push --force`, aunque **ojo**, si algun colega ya se trajo por algun motivo los cambios de esa rama (incluyendo mi último commit), no verá el archivo agregado hasta volver a hacer pull, por lo que no se recomienda forzar los cambios si es una rama en la que esta trabajando mas de uno, y en caso de ser necesario avisar con antelacion a los colegas involucrados, para evitar resolver conflictos luego al subir cambios con ese commit modificado.

   En resumen: \
   Si no hice push: `git add <archivo_olvidado>` `git commit --amend <--no-edit>` `git push`.\
   Si ya hice push: `git add <archivo_olvidado>` `git commit --amend <--no-edit>` `git push --force`.

2. Si has trabajado con control de versiones ¿Cuáles han sido los flujos con los que has
   trabajado?
   - Con Git flow y Github flow principalmente, aunque en Uber particularmente con un flujo un poco distinto, en que el la Pull request era mas parecido a un patch debido a que se usaba phabricator aún, y cada quien usaba su flujo preferido en su entorno local.
3. ¿Cuál ha sido la situación más compleja que has tenido con esto?
   - Nada muy terrible, cuando llevaba poco tiempo usando git en un repositorio de una startup que tuve, se me olvido editar el archivos `.gitignore` y se me pasaron muchas imagenes, tantas que superamos el tamaño limite de repositorio gratis para ese tiempo, ya luego en otros cargos fuera de trabajar con multiples ramas, canary, beta, QA etc, y jugar con feature flags nada mas complejo honestamente, resolver conflictos mas que nada.
4. ¿Qué experiencia has tenido con los microservicios?
   - Diría que que mas que un poco, mientras trabajé en Elun, migramos partes de un monolito antiguo de Copec hecha en Django a una serie de APIs, que hicimos desde 0 con FastAPI y Flask, todo montado con Docker, traefik, y corriendo en EC2 de AWS, con un CI/CD básico con bitbucket actions, ssh. Luego en Uber de nuevo con sus microservicios.
5. ¿Cuál es tu servicio favorito de GCP o AWS? ¿Por qué?
   - Puedo decir azure, na broma, prefiero AWS por rapidez, claridad y por que bajo mi punto de vista hay mas documentacion, pero al final da igual, he usado ambos y se pueden usar ambos a la vez, cada cual conforme a conveniencia o necesidades de cada software a desplegar.
