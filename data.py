# -*- coding: utf-8 -*-
#q 57
#ans 50
#em 38
questions = [
	'¿Qué harías si un grupo de niños te persigue y te molesta?',
	'¿Qué harías si un compañero  te obliga a sacarle plata del bolso de tu profesora porque de lo contrario te golpea?',
	'¿Qué harías si una amiga te quita un cuaderno con el que debes presentar una tarea?',
	'¿Qué harías si en un bus un extraño te ofrece algo de tomar y tu tienes mucha sed?',
	'¿Qué harías si en el parque se acerca una persona muy amable y te pide que la acompañes a un lugar donde vas a divertirte?',
	'Tomás le tiene miedo a la oscuridad y a los truenos. ¿Qué puede hacer Tomás para enfrentar esta situación?',
	'¿Qué harías si empiezas a pelear frecuentemente con tu hermana menor?',
	'¿Qué harías si estás en  casa y mientras te vistes después de bañarte, te das cuenta que un conocido  te está mirando a escondidas?',
	'¿Qué harías si en un café internet una conocida de tu familia se te acerca y te invita a ir a su casa y prestarte el computador gratis?',
	'¿Qué harías tu si camino a casa después de ir a la escuela hay un perro muy bravo que empieza a ladrarte?',
	'¿Qué podrían hacer tus papás si ellos se pelearan cada vez que a ti o a tus hermanos les va mal en el colegio?',
	'¿Qué harías si en una fiesta, alguien conocido de tu familia se te acerca y empieza a tocar tus partes privadas?',
	'Vas con una amiga, y una pareja muy elegante que has visto varias veces en la calle les dice que les quieren tomar unas fotos para una revista famosa. ¿Qué harías?',
	'¿Qué harías si en el barrio un vecino adulto te invita a entrar a su casa para tomar algo y ver tu película favorita?',
	'Luis se puso el saco favorito de su hermano sin pedirle permiso. Al darse cuenta, el hermano le pegó y le prohibió tocar sus cosas. ¿De qué otra manera puede actuar el hermano?',
	'En la final del campeonato Orlando y Gabriel se pusieron a discutir porque Orlando cometió una falta y por eso el equipo contrario metió un gol. ¿Cómo resolver este conflicto?',
	'¿Qué harías si te peleas con un amigo porque no tapó un penal y el equipo contrario ganó el campeonato del barrio?',
	'¿Qué harías si por estar jugando le rompes el lápiz a una amiga que no tiene más lápices?',
	'¿Qué harías si estando solo en la casa un extraño te pide que le abras la puerta porque han enviado un regalo para la familia?',
	'¿Qué harías tu si un conocido de la familia te ofrece dulces y dinero y te invita a su casa a ver tu película favorita?',
	'¿Qué harías si un niño o niña más grande que tú, te ofrece dinero para que le quites algo a un niño o niña de tu edad?',
	'Cada vez que deben hacer ejercicios de matemáticas en grupo  Lina pelea con su amiga Nelly porque ella no entiende lo que debe hacer. ¿Qué puede hacer Lina en lugar pelear con Nelly?',
	'Rosario se peleó con Silvia e hizo que todas sus amigas también se pelearan con ella y no le hablaran. ¿Qué otra alternativa tienen las amigas de Rosario?',
	'¿Qué solución propones si cada vez que le desobedeces a tu mamá las dos gritan y pelean?',
	'¿Qué harías si cuando tu amiga se enoja contigo llora y te pega?',
	'Discutes con tu amigo porque no hizo su parte de un trabajo en clase. La profesora quiere ayudarles a resolver sus diferencias. ¿Qué puede hacer?',
	'¿Qué harías si al ir a casa de tu vecina solo está su esposo y el señor te invita a seguir y te ofrece golosinas?',
	'¿Qué harías si un amigo de la familia te invita a su casa y te promete darte dulces si te dejas tomar unas fotos?',
	'¿Qué harías si un vecino te invita a entrar a su casa a solas, te da regalos y te pide que no le cuentes a nadie?',
	'Elena peleó con María, su mejor amiga, porque María se hizo novia de Diego, el exnovio de Elena. Elena se sintió traicionada. ¿Qué otra cosa hubiera podido hacer Elena?',
	'¿Qué harías si cada vez que estás viendo TV con tus hermanos cada uno quiere ver un programa diferente?',
	'Celina habla mal de sus compañeros en facebook porque le ponen apodos. ¿Qué otra opción tiene Celina?',
	'Te enojas con tu hermana porque no lavó la loza del almuerzo aunque el turno le tocaba a ella. Pelean y se golpean. ¿Cómo resolver este problema?',
	'¿Qué harías si al salir del colegio una persona muy elegante te invita a trabajar en una agencia de modelos y ganar mucho dinero si te dejas tomar fotos?',
	'¿Qué harías tu si estando en casa jugando con tus hermanos uno de ellos se cae y se causa una herida?',
	'Cada vez que juega tu equipo favorito, el vecino te invita a verlo en su casa y te da regalos. Te dice que no le cuentes a tus hermanos. ¿Consideras que esto está bien?',
	'El gato de Leonor dañó la blusa de Susana, su hermana mayor. Susana quiere sacar al gato de la casa. ¿Cómo resolver este problema?',
	'Francisco e Isabel pelean a diario porque Isabel se demora mucho en el baño y Francisco casi siempre llega tarde al colegio por esa razón. ¿Qué se puede hacer para resolver este problema?',
	'Dejaste tu helado favorito en la mesa y tu hermanita lo derramó. Te enojaste y le pegaste. ¿Qué puedes hacer en lugar de golpearla?',
	'Estabas jugando con tu hermanito menor y él se enojó cuando ganaste porque era él quien quería ganar. ¿Cómo resolver este conflicto?',
	'Cada vez que alguien le hace algo a tu hermano, que a él no le gusta, grita y  tira cosas. ¿Cómo puede responder mejor a esta situación?',
	'¿Qué harías si cada vez que traes al colegio tu balón de fútbol, peleas con tu mejor amigo porque él no sabe jugar fútbol y tu sí?',
	'Aunque varias veces has dicho que no, el señor del aseo en el colegio te ha ofrecido varias veces acompañarte a casa al terminar las clases. ¿Qué puedes hacer?',
	'Un vecino le da dinero a un amigo tuyo y a veces le toca la pierna y lo abraza. El señor le dice a tu amigo que si es obediente lo va a cuidar y le va a dar dinero. ¿Qué puede hacer tu amigo?'
]
answers = [
	[
		['Me detengo y les exijo que me respeten y me dejen tranquilo',1],
		['Los amenazo con contarle a un adulto',0],
		['Me escondo hasta que se vayan',0]
	],
	[
		['Le digo que NO y me voy',0],
		['Le digo que NO, que eso está mal y que yo no voy a hacer algo que considero inadecuado.',1],
		['Le obedezco porque me da miedo que me haga daño',0]
	],
	[
		['Decirle a tu profesora quién te quitó el cuaderno, para que ella obligue a tu amigo a devolvértelo.',0],
		['Decirle firmemente a tu amiga (es decir sin llorar ni gritar), que te devuelva tu cuaderno',1],
		['Quitarle un cuaderno a mi amiga para que ella sienta lo mismo que yo',0]
	],
	[
		['Acepto porque no me aguanto la sed',0],
		['Le pido permiso a mi mamá o a mi papá para aceptar el ofrecimiento',0],
		['Le digo que NO, no me dejo convencer y me alejo de él',1]
	],
	[
		['Le digo que NO y me voy a seguir jugando',0],
		['Le digo que NO, me alejo y le cuento lo sucedido a un adulto de mi confianza',1],
		['Le digo que NO porque no se lo que voy a hacer allá',0]
	],
	[
		['Tomás puede buscar a alguien de su confianza para que lo acompañe cuando esto suceda',1],
		['Tomás puede esconderse o buscar un lugar donde se sienta seguro',0],
		['Tomás debe buscar cómo distraerse mientras esté en esas situaciones',0]
	],
	[
		['No se puede hacer nada, es normal que los hermanos peleen',0],
		['Buscar a mi mamá para que ella resuelva el problema',0],
		['Podemos expresar nuestros sentimientos, respetarnos mutuamente y aprender a ceder.',1]
	],
	[
		['Gritarle que se vaya y que me respete',0],
		['Taparme, decirle que se retire y contarle lo sucedido a un adulto de mi confianza',1],
		['Decirle que se retire y que respete mi espacio personal',0]
	],
	[
		['Decirle que NO y alejarme de ella',0],
		['No volver a ir sola al café internet',0],
		['Decirle que NO, alejarme y contarle inmediatamente a un adulto de mi confianza',1]
	],
	[
		['Me asusto y empiezo a llorar',0],
		['Respiro calmadamente y me mantengo a distancia hasta que el perro se calme',1],
		['Espero hasta que venga un adulto a ayudarme',0]
	],
	[
		['Dialogar entre ellos',0],
		['No pelear delante de sus hijos',0],
		['Crear acuerdos sobre la manera de ayudar a sus hijos',1]
	],
	[
		['Decirle que NO, alejarme y contarle inmediatamente a un adulto de mi confianza',1],
		['Decirle que NO porque yo tengo derecho a ser respetado',0],
		['Decirle que NO y gritar para que todos se den cuenta',0]
	],
	[
		['No aceptar la invitación de la pareja porque aunque se vean muy amables, son personas extrañas',0],
		['No aceptar la invitación, alejarse de la pareja y contarle a un adulto de su confianza lo sucedido',1],
		['Aceptar la invitación de la pareja con la condición de que les tomen las fotos en el parque o en un lugar público',0]
	],
	[
		['Le agradezco, le digo que NO y luego le cuento a un adulto de mi confianza',1],
		['Salgo corriendo asustado',0],
		['Acepto la invitación porque es un vecino conocido',0]
	],
	[
		['Escondiéndole a Luis su juguete favorito',0],
		['Hablando con el hermano sobre el respeto a las cosas de los demás y solicitándole que le entregue el saco limpio como estaba',1],
		['Contándole a la mamá para que lo castigue y prohibiéndole al Luis que coja sus cosas',0]
	],
	[
		['Orlando debe aceptar su error y pedirle disculpas a sus compañeros',0],
		['Orlando puede tranquilizar a Gabriel y hacer su mejor esfuerzo para ganar el partido',0],
		['Orlando y Gabriel deben concentrarse en jugar mejor y tratar de hacer goles antes que dejarse llevar por el enojo',1]
	],
	[
		['Decirle a mi amigo que practique para aprender a tapar penales',0],
		['No debo enojarme porque un error lo comete cualquier persona',0],
		['Hablar sobre lo que sentí cuando Alejandro no tapó el penal.',1]
	],
	[
		['Le digo a mi amiga que le rompí el lápiz sin intención',0],
		['Me disculpo con mi amiga y le consigo otro lápiz',1],
		['Me quedo callada y espero a que mi amiga encuentre un nuevo lápiz',0]
	],
	[
		['Le dices que NO y no le hablas más',0],
		['Le dices que NO y no le abres la puerta porque tu no hablas con extraños',1],
		['Le dices que sí y le abres la puerta porque a tí te encantan las sorpresas',0]
	],
	[
		['Le digo que NO porque mi mamá no me ha dado permiso',0],
		['Le digo que NO porque yo no puedo salir solo',0],
		['Le digo que NO, le cuento a una persona de mi confianza y evito estar a solas con esa persona.',1]
	],
	[
		['Le digo que no y le pido ayuda a un adulto de mi confianza.',1],
		['Le digo que si porque me da miedo que me pegue',0],
		['Le digo que sí pero luego le cuento a la profesora',0]
	],
	[
		['Pedirle que estudie más para que le vaya bien',0],
		['Explicarle lo que ella no entendió y trabajar en equipo con ella sin enojarse',1],
		['Hacer los ejercicios con otros amigos y no con Nelly',0]
	],
	[
		['Ser  amigas de Silvia a escondidas',0],
		['Decirle a Rosario que respetan lo que ella piensa y siente pero que no condicione su amistad a hacer solo lo que ella espera',1],
		['Alejarse de Rosario porque las obliga a hacer algo con lo que ellas no están de acuerdo',0]
	],
	[
		['Deberías hacer caso a tu mamá siempre para evitar esta situación',0],
		['Tu mamá debería comprenderte y no gritarte',0],
		['Hablar cuando no estemos enojadas diciendo lo que sentimos y estableciendo acuerdos.',1]
	],
	[
		['Decirle que no se desquite conmigo y pedirle que me deje tranquila',0],
		['Pedirle a la profesora que la cambie de puesto',0],
		['Decirle a mi amiga cómo me siento cada vez que ella actúa así y contarle a un adulto de mi confianza para que me oriente sobre cómo actuar',1]
	],
	[
		['Darles una nueva oportunidad para presentar el trabajo',0],
		['Que cada uno escuche al otro: sus razones, emociones y deseos para luego llegar a un acuerdo',1],
		['Que entre ellos arreglen el problema y presenten el trabajo completo',0]
	],
	[
		['Entrar porque el vecino es una persona conocida y amable',0],
		['Le digo que vuelvo más tarde cuando llegue la vecina.',0],
		['Le digo NO gracias, vuelvo casa  y le cuento a mi mamá lo sucedido',1]
	],
	[
		['Acepto su invitación',0],
		['Le digo que NO y me alejo',0],
		['Le digo NO y le cuento a un adulto de mi confianza',1]
	],
	[
		['Acepto los regalos porque me da lo que siempre he querido.',0],
		['Acepto los regalos y le cuento a mis papás.',0],
		['No acepto los regalos y le cuento a mis padres acerca de esta situación.',1]
	],
	[
		['Hablar con María sobre sus sentimientos para que ella entendiera lo que significaba esa situación',1],
		['Escribirle una carta a María pidiéndole que no se metiera con el exnovio de ella',0],
		['Pedirle a sus otras amigas que aconsejaran a María',0]
	],
	[
		['Hacer un trato: el que llega primero es el que coge el control del televisor',0],
		['El que no le guste el programa se va a hacer otra cosa',0],
		['Hacer turnos de tal manera que primero tiene uno el control y luego el turno le toca al siguiente',1]
	],
	[
		['Hacer la lista de los que la molestan y entregár- sela a la profesora para que ella los sancione',0],
		['Contarle a su hermano mayor lo que está sucediendo para que la defienda',0],
		['Hablar con la profesora para que ella hable con los niños. Celina debe respetar y exigir respeto a sus compañeros.',1]
	],
	[
		['Ambas deben calmarse, escucharse y establecer un acuerdo que deben cumplir',1],
		['Llamando a tu mamá para que regañe a tu hermana que no hizo lo que tocaba',0],
		['La hermana menor debe cumplir con su deber y asumir las consecuencias por no cumplir con lo que le tocaba',0]
	],
	[
		['Aceptar la invitación porque es una oportunidad que no se ofrece a muchas personas',0],
		['Acepto la invitación  si me toma las fotos en el parque o en un lugar público',0],
		['No acepto la invitación, me alejo y le cuento a un adulto de su confianza lo sucedido',1]
	],
	[
		['Le digo que se calle y que no le cuente nada a mis papás',0],
		['Busco algo con qué curarlo',0],
		['Llamo a mi mamá y le cuento lo sucedido para que ella me indique lo que debo hacer',1]
	],
	[
		['Está bien porque los regalos son solo una muestra de cariño sin ningún interés',0],
		['No está bien porque el vecino es un señor y no debería darle regalos a un niño',0],
		['No está bien porque el vecino me pide que guarde el secreto',1]
	],
	[
		['Disculparse con Susana y llegas a acuerdos sobre la situación. Susana a su vez puede hablar con su hermana sobre cómo se sentiría ella si el gato se fuera.',1],
		['Leonor puede pedirle a su hermana que la perdone y prometerle que algo así no volverá a suceder',0],
		['Leonor debe castigar al gato y ahorrar para comprarle una nueva blusa a su hermana',0]
	],
	[
		['Francisco puede levantarse más temprano para bañarse primero ',0],
		['Pueden hacer turnos semanales e Isabel tener un tiempo límite para estar en el baño',1],
		['Deben hablar con la mamá para que les ayude a resolver la situación',0]
	],
	[
		['Estar pendiente y no dejar tus cosas para que tu hermana las coja',0],
		['Regañarla y no pegarle para que esto no vuelva a suceder',0],
		['Respirar profundo antes de tomar cualquier decisión y luego hablar con tu hermanita para enseñarle sobre el respeto a las cosas de los demás',1]
	],
	[
		['Puedes ayudarle a tu hermanito dejándolo ganar de vez en cuando',0],
		['Pueden hablar sobre lo sucedido para que el niño aprenda que a veces se gana y a veces no',0],
		['Puedes ayudar a tu hermano escuchándolo sobre lo que siente por haber perdido y poniéndote en su lugar para entender por qué reaccionó así',1]
	],
	[
		['Desahogarse pegándole a algo y no a alguien',0],
		['Respirar profundo, contar hasta 10 y pensar antes de actuar',0],
		['Respirar profundo para calmarse y aprender cómo manejar su ira ',1]
	],
	[
		['Puedo enseñarle a mi amigo a jugar fútbol para que nos divirtamos juntos',0],
		['Puedo jugar con mi amigo otras cosas que nos gusten a los dos',1],
		['Lo mejor es no volver a llevar el balón para evitar conflictos con mi amigo',0]
	],
	[
		['Aceptar el ofrecimiento del señor para no irme sola a la casa',0],
		['No permitir que el señor me convenza,decirle que NO y contarle lo sucedido a un adulto de confianza',1],
		['Decirle a una amiguita que me espere para que el señor nos acompañe a las dos',0]
	],
	[
		['NO debe seguir aceptando el dinero y contarle a un adulto de confianza lo que sucede para que lo oriente',1],
		['NO debe seguir aceptando el dinero del vecino porque los adultos no deben tocar a los niños',0],
		['NO debe volver a estar a solas con el vecino y alejarse de él.',0]
	]
]
emotions = [
	['Te sientes así cuando alguna persona te ayuda a resolver un problema o hace algo por tí sin esperar nada a cambio. Además te puedes sentir apoyado, entendido, escuchado.',3],
	['Cuando te sientes de esta manera te da tristeza, extrañas a las personas que amas y quisieras estar cerca de ellas',17],
	['Cuando otros manifiestan esto hacia ti te sientes bien porque se interesan por conocerte y por saber cómo eres.',2],
	['Este sentimiento puede surgir cuando te culpan por algo que no hiciste o cuando alguien te hace daño y consideras que no tienes cómo defenderte de esta situación.',15],
	['Cuando te sientes así puedes experimentar enojo, rabia. Esto puede ocurrir cuando no logras algo que te has propuesto o cuando alguien no te cree aunque dices la verdad.',9],
	['Cuando estás así, no sabes qué hacer, tienes dos o más opciones y no sabes cuál elegir. En otras ocasiones te ocurre porque no entiendes lo que está sucediendo.',6],
	['Te puedes sentir así cuando te tienen en cuenta o piden tu opinión para tomar una decisión; también cuando te das cuenta que puedes hacer bien algo',10],
	['Cuando estás así puedes sentir que no sabes qué hacer. Te sudan las manos o la cara, el corazón palpita muy rápido, las piernas te tiemblan y no sabes qué decir o qué hacer.',12],
	['Te sientes así cuando confías en alguien y esa persona traiciona tu confianza. Eso significa que puedes sentir rabia y tristeza a la vez y tal vez creas que no puedes confiar en nadie.',7],
	['Te puedes sentir así cuando debes cumplir con una tarea que alguien te ha asignado y sabes que no debes fallar.',16]
]