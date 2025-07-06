# Project_template


# Задание 1. Анализ и планирование

<aside>

Чтобы составить документ с описанием текущей архитектуры приложения, можно часть информации взять из описания компании и условия задания. Это нормально.

</aside>

### 1. Описание функциональности монолитного приложения


Нынешнее приложение компании позволяет только управлять отоплением в доме и проверять температуру.
Каждая установка сопровождается выездом специалиста по подключению системы отопления в доме к текущей версии системы.


**Управление отоплением:**

- Пользователи могут удалённо включать/выключать отопление в своих домах через веб-интерфейс.
- Специалисты по поддержке могут подключать новые модули управления отоплением. Самостоятельно подключить свой датчик к системе обычный пользователь не может 
- Система поддерживает включение/выключение отопления через веб интерфейс 
- Система поддерживает подключение новых модулей для управления отоплением. Каждая установка сопровождается выездом специалиста по подключению системы отопления в доме к текущей версии системы

**Мониторинг температуры:**

- Пользователи могут просматривать текущую температуру в своих домах через веб-интерфейс.
- Система поддерживает получение данных о температуре с датчиков, установленных в домах. Данные о температуре обновляются по запросу от сервера

### 2. Анализ архитектуры монолитного приложения

Перечислите здесь основные особенности текущего приложения: какой язык программирования используется, какая база данных, как организовано взаимодействие между компонентами и так далее.

Архитектура приложения представляет из себя монолит:
- Архитектура монолитная, все компоненты системы (обработка запросов, бизнес-логика, работа с данными) находятся в рамках одного приложения.
- Масштабируемость ограничена, так как монолит сложно масштабировать по частям
- Развертывание требует остановки всего приложения.
- Язык программирования Go  
- СУБД Postgres 
- Все взаимодействия синхронные, запросы обрабатываются последовательно. Никаких асинхронных вызовов и реактивного взаимодействия в системе нет. 
- Управление идёт от сервера к датчику 
- Данные о температуре получаются через запрос от сервера к датчику

### 3. Определение доменов и границы контекстов

Опишите здесь домены, которые вы выделили.

- Домен "Управление отоплением": это основной домен, который компания уже предоставляет и он остается важной частью новой экосистемы
	- Поддомен "Управление отоплением" 
		- Контекст "Управление устройствами отопления": отвечает за управление физическими устройствами отопления (котлы, радиаторы, теплые полы). Включение/выключение, установка температуры, получение информации о состоянии устройства.
	- Поддомен "Мониторинг температуры": Собирает и хранит данные о температуре с датчиков. Функции: получение данных с датчиков, агрегация данных.
		- Контекст "сбор и предоставление данных о температуре" 
- Домен "Управление освещением": позволяет пользователям контролировать освещение в доме, что является стандартной функцией умного дома.
	- Поддомен "Управление устройствами освещения"
		- Контекст "управление устройством освещения": включение выключения освещения, проверка состояния освещения
	- Поддомен "Управление группами освещения" (комнаты и уличное освещение)
		- Контекст "управление группой освещения": включение выключения группы освещения, проверка состояния группы освещения
- Домен "Управление воротами": обеспечивает удаленное управление воротами, добавляя безопасность 
	- Поддомен "Управление устройствами ворот" 
		- Контекст "управление состоянием ворот"(открытие/закрытие)
	- Поддомен "Мониторинг состояния ворот"
		- Контекст "мониторинг состояния ворот и сигнализация": мониторинг состояния ворот и отправка уведомлений о любых подозрительных событиях
- Домен "Наблюдение": позволяет пользователям удаленно наблюдать за своим домом, повышая безопасность и контроль. 
	- Поддомен "Управление камерами"
		- Контекст "настройка камер"
	- Подомен "Просмотр камер" 
		- Контекст "просмотр видео с камер"
	- Поддомен "Запись видео"
		- Контекст "управление видеоархивом": запись видео, хранение архива и предоставление доступа к записям
	- Подомен "Детекция событий"
		- Контекст "детекция событий и уведомления": анализ видеопотока, обнаружение событий и отправка уведомлений пользователю
- Домен "Администрирование"
	- Подомен "Управление пользователями"
		- Контекст "управление пользователями и доступом к устройствам"
	- Подомен "Подключение устройств"  
		- Контекст "подключение новых устройств": подключение новых устройств, которые поддерживаются платформой

Домен "Управление отоплением" - это существующее решение, которое будет подвергнуто рефакторингу и разделено на микросервисы. Эта подсистема станет первым релизом после рефакторинга, что позволит команде разработчиков быстро получить представление о функционировании микросервисной архитектуры и оперативно внести необходимые изменения в процесс разработки. Станет понятно, как лучше масштабировать эту и другие подсистемы в контексте микросервисной архитектуры и можно будет оперативно скорректировать стратегию. Масштабирование может отличаться от других доменов.

### **4. Проблемы монолитного решения**

- Ограниченная масштабируемость, потому что монолит сложно масштабировать по частям. Это значит что существующая система просто не справиться с нагрузкой при увеличении количества подключённых домов.  
- Сбой в одной части системы ведёт к остановке всей системы
- Обновление требует остановки всей системы
- Добавление новой функциональности со временем станет просто невозможным, а релизы будут выпускаться очень долго и тяжело тестироваться.  
- Невозможно привлечь несколько команд для разработки из-за того что кодовая база одна и система очень сильно связана на уровне компонентов и кода. 

### 5. Визуализация контекста системы — диаграмма С4

Добавьте сюда диаграмму контекста в модели C4.

Диаграмма контекста C4 для исходного монолита:

```puml

@startuml
title Warmhouse Context Diagram

top to bottom direction

!includeurl https://raw.githubusercontent.com/RicardoNiepel/C4-PlantUML/master/C4_Component.puml

Person(user1, "User", "Жители домов")

System(WarmhouseSystem, "Warmhouse System", "Отопление, освещение, ворота, наблюдение")
System(WarmSystem, "Устройства отопления", "Котлы, радиаторы, теплые полы")

Rel(user1, WarmhouseSystem, "Использует систему")
Rel(WarmhouseSystem, WarmSystem, "Управление и получение данных")

@enduml

```

Диаграмма контекста C4 для нового решения:

```puml

@startuml
title Warmhouse Context Diagram

top to bottom direction

!includeurl https://raw.githubusercontent.com/RicardoNiepel/C4-PlantUML/master/C4_Component.puml

Person(user1, "User", "Жители домов")

System(WarmhouseSystem, "Warmhouse System", "Отопление, освещение, ворота, наблюдение")
System(WarmSystem, "Устройства отопления", "Котлы, радиаторы, теплые полы")
System(GatesSystem, "Ворота", "")
System(LightSystem, "Освещение", "")
System(VideoSystem, "Наблюдение", "")

Rel(user1, WarmhouseSystem, "Использует систему")
Rel(WarmhouseSystem, WarmSystem, "Управление и получение данных")
Rel(WarmhouseSystem, GatesSystem, "Управление и получение данных")
Rel(WarmhouseSystem, LightSystem, "Управление и получение данных")
Rel(WarmhouseSystem, VideoSystem, "Управление и получение данных")

@enduml

```

# Задание 2. Проектирование микросервисной архитектуры

В этом задании вам нужно предоставить только диаграммы в модели C4. Мы не просим вас отдельно описывать получившиеся микросервисы и то, как вы определили взаимодействия между компонентами To-Be системы. Если вы правильно подготовите диаграммы C4, они и так это покажут.

**Диаграмма контейнеров (Containers)**

```puml

@startuml
title Warmhouse Container Diagram

top to bottom direction

!includeurl https://raw.githubusercontent.com/RicardoNiepel/C4-PlantUML/master/C4_Container.puml

Person(user, "User", "Пользователь системы Умный дом")
System(WarmhouseSystem, "Warmhouse System", "Отопление, освещение, ворота, наблюдение")

Container_Boundary(WarmhouseSystem, "FitLife System") {
  Container(ApiApp, "API Application (IPI)", "Python, Fast API", "Обрабатывает пользовательские запросы, управление пользователями и устройствами")
  
  Container(HeatingControlService, "Heating control service", "Python", "Управление отоплением")
  Container(TemperatureMonitoringService, "Temperature monitoring service", "Python", "Мониторинг температуры")
  Container(TemperatureDatabase, "Monitoring database", "PostgreSQL/TimescaleDB", "Хранит данные мониторинга температуры")
  
  Container(LightControlService, "Light control service", "Python", "Управление освещением")
  
  Container(GateControlService, "Gate control service", "Python", "Управление воротами")
  Container(GateMonitoringService, "Gate monitoring service", "Python", "Отслеживание состояния ворот")
  
  Container(VideoCameraService, "Video and Camera Service", "Python", "Управление видеоархивом, просмотр камер и детекция движения")
  Container(VideoDatabase, "Video database", "PostgreSQL", "Хранит видео и информацию о движении")
  
  Container(UsersDatabase, "Users database", "PostgreSQL", "Хранение данных о пользователях")
  Container(CommonDeviceService, "Common device service", "Python", "Регистрация/удаление/активация/деактивация устройств. Получение списка устройств для пользователя")
  Container(DeviceCatalogDatabase, "DeviceCatalog database", "PostgreSQL", "Хранит данные о подключенных устройствах, а также их настройки")

}

System(HeatingModuleSystem, "Heating module", "Модуль управления отоплением")
System(LightControlModule, "Light control module", "Модуль управления освещением")
System(GateModule, "Gate module", "Модуль управления воротами")
System(CameraModule, "Camera module", "Модуль работы с камерами")

Rel(user, ApiApp, "Uses the system")

Rel(ApiApp, HeatingControlService, "Управление отоплением и запрос телеметрии")
Rel(ApiApp, LightControlService, "Управляет освещением")
Rel(ApiApp, GateControlService, "Управляет воротами")
Rel(ApiApp, VideoCameraService, "Управляет и получает данные наблюдения")

Rel(ApiApp, GateMonitoringService, "Следит за состоянием ворот")
Rel(ApiApp, TemperatureMonitoringService, "Настройка мониторинга и получение данных мониторинга")

Rel(ApiApp, UsersDatabase, "Управление пользователями и хранение данных")
Rel(ApiApp, CommonDeviceService, "Регистрация и управление устройствами")
Rel(CommonDeviceService, DeviceCatalogDatabase, "Чтение и запись данных устройств")

Rel(LightControlService, LightControlModule, "Управляет модулем освещения")

Rel(GateControlService, GateModule, "Управляет модулем ворот")
Rel(GateMonitoringService, GateModule, "Проверяет ворота")

Rel(VideoCameraService, VideoDatabase, "Запись и чтение видео и данных детекции движения")
Rel(VideoCameraService, CameraModule, "Получение видео с камеры в реальном времени и анализ")

Rel(HeatingControlService, HeatingModuleSystem, "Управляет")
Rel(TemperatureMonitoringService, TemperatureDatabase, "Сохранение и предоставление данных мониторинга")
Rel(TemperatureMonitoringService, HeatingModuleSystem, "Получает данные мониторинга")

' Доступ к каталогу устройств для всех сервисов
Rel(ApiApp, CommonDeviceService, "Доступ к каталогу устройств")
Rel(HeatingControlService, CommonDeviceService, "Доступ к каталогу устройств")
Rel(LightControlService, CommonDeviceService, "Доступ к каталогу устройств")
Rel(GateControlService, CommonDeviceService, "Доступ к каталогу устройств")
Rel(VideoCameraService, CommonDeviceService, "Доступ к каталогу устройств")
Rel(GateMonitoringService, CommonDeviceService, "Доступ к каталогу устройств")
Rel(TemperatureMonitoringService, CommonDeviceService, "Доступ к каталогу устройств")

@enduml

```

**Диаграмма компонентов (Components)**

Добавьте диаграмму для каждого из выделенных микросервисов.

```puml

@startuml
title Api application - Component Diagram

skinparam rectangle {
  BackgroundColor #D0E1F9
  BorderColor black
  BorderThickness 1
  RoundCorner 10
}

rectangle "API Application" as ApiApp {
  rectangle "FastAPI (REST API)" as fastApi
  rectangle "User Manager" as userManager
  rectangle "Device Manager" as deviceManager
  rectangle "Command Processor" as commandProcessor
}

rectangle "Users Database" as usersDb #FFE4E1
rectangle "Common Device Service API" as commonDeviceApi #FFE4E1
rectangle "Heating Control Service API" as heatingControlApi #FFE4E1
rectangle "Light Control Service API" as lightControlApi #FFE4E1
rectangle "Gate Control Service API" as gateControlApi #FFE4E1
rectangle "Video & Camera Service API" as videoCameraApi #FFE4E1
rectangle "Temperature monitoring service API" as temperatureMonitoringApi #FFE4E1
rectangle "Gate monitoring service API" as gateMonitoringApi #FFE4E1

fastApi --> userManager 
fastApi --> deviceManager
fastApi --> commandProcessor

userManager --> usersDb : SQL доступ
deviceManager --> commonDeviceApi : REST
commandProcessor --> heatingControlApi : REST
commandProcessor --> lightControlApi : REST
commandProcessor --> gateControlApi : REST
commandProcessor --> videoCameraApi : REST
commandProcessor --> temperatureMonitoringApi : REST
commandProcessor --> gateMonitoringApi : REST

@enduml

```



```puml

@startuml
title HeatingControlService - Component Diagram

skinparam rectangle {
  BackgroundColor #FFE4B5
  BorderColor black
  BorderThickness 1
  RoundCorner 10
}

rectangle "Heating Control Service" as heatingService {
  rectangle "API" as api
  rectangle "Command Handler" as commandHandler
  rectangle "Heating Module Client" as heatingModuleClient
}

rectangle "Heating Module System" as heatingModuleSystem #FFE4E1

api --> commandHandler : принимает команды
commandHandler --> heatingModuleClient : отправляет команды

heatingModuleClient --> heatingModuleSystem : управление модулем отопления

@enduml

```



```puml

@startuml
title TemperatureMonitoringService - Component Diagram

skinparam rectangle {
  BackgroundColor #D3F9D8
  BorderColor black
  BorderThickness 1
  RoundCorner 10
}

rectangle "Temperature Monitoring Service" as tempMonitorService {
  rectangle "API" as api
  rectangle "Data Collector" as dataCollector
  rectangle "Data Processor" as dataProcessor
  rectangle "Database Client" as dbClient
  rectangle "Alert Manager" as alertManager
}

rectangle "Temperature Database" as temperatureDb #FFE4E1
rectangle "Heating Module System" as heatingModuleSystem #FFE4E1

api --> dataCollector : настройка мониторинга
dataCollector --> heatingModuleSystem : получение данных
dataCollector --> dataProcessor : передача данных
dataProcessor --> dbClient : сохранение данных
dataProcessor --> alertManager : анализ и уведомления
dbClient --> temperatureDb : SQL доступ

@enduml

```


```puml

@startuml
title LightControlService - Component Diagram

skinparam rectangle {
  BackgroundColor #FFFACD
  BorderColor black
  BorderThickness 1
  RoundCorner 10
}

rectangle "Light Control Service" as lightService {
  rectangle "API" as api
  rectangle "Command Handler" as commandHandler
  rectangle "Light Module Client" as lightModuleClient
}

rectangle "Light Control Module" as lightModule #FFE4E1

api --> commandHandler : принимает команды
commandHandler --> lightModuleClient : отправляет команды

lightModuleClient --> lightModule : управление модулем освещения

@enduml

```


```puml

@startuml
title GateControlService - Component Diagram

skinparam rectangle {
  BackgroundColor #FFDAB9
  BorderColor black
  BorderThickness 1
  RoundCorner 10
}

rectangle "Gate Control Service" as gateService {
  rectangle "API" as api
  rectangle "Command Handler" as commandHandler
  rectangle "Gate Module Client" as gateModuleClient
}

rectangle "Gate Module" as gateModule #FFE4E1

api --> commandHandler : принимает команды
commandHandler --> gateModuleClient : отправляет команды

gateModuleClient --> gateModule : управление модулем ворот

@enduml

```


```puml

@startuml
title GateMonitoringService - Component Diagram

skinparam rectangle {
  BackgroundColor #E6E6FA
  BorderColor black
  BorderThickness 1
  RoundCorner 10
}

rectangle "Gate Monitoring Service" as gateMonitorService {
  rectangle "API" as api
  rectangle "State Collector" as stateCollector
  rectangle "Alert Manager" as alertManager
  rectangle "Gate Module Client" as gateModuleClient
}

rectangle "Gate Module" as gateModule #FFE4E1

api --> stateCollector : запрос статусов
stateCollector --> gateModuleClient : получение данных
stateCollector --> alertManager : анализ состояния

gateModuleClient --> gateModule : получение данных с модуля ворот

@enduml

```


```puml

@startuml
title VideoCameraService - Component Diagram

skinparam rectangle {
  BackgroundColor #D1EEEE
  BorderColor black
  BorderThickness 1
  RoundCorner 10
}

rectangle "Video & Camera Service" as videoCameraService {
  rectangle "API" as api
  rectangle "Video Recorder" as videoRecorder
  rectangle "Camera Viewer" as cameraViewer
  rectangle "Motion Detector" as motionDetector
  rectangle "Video Database Client" as videoDbClient
  rectangle "Camera Module Client" as cameraModuleClient
}

rectangle "Video Database" as videoDb #FFE4E1
rectangle "Camera Module" as cameraModule #FFE4E1

api --> videoRecorder : команды записи
api --> cameraViewer : запрос видео
api --> motionDetector : запуск анализа

videoRecorder --> videoDbClient : запись видео
motionDetector --> videoDbClient : запись метаданных

videoRecorder --> cameraModuleClient : получение видео
cameraViewer --> cameraModuleClient : просмотр видео
motionDetector --> cameraModuleClient : анализ видео

videoDbClient --> videoDb : SQL доступ
cameraModuleClient --> cameraModule : получение видео с камер

@enduml

```


```puml

@startuml
title CommonDeviceService - Component Diagram

skinparam rectangle {
  BackgroundColor #F0E68C
  BorderColor black
  BorderThickness 1
  RoundCorner 10
}

rectangle "Common Device Service" as commonDeviceService {
  rectangle "API" as api
  rectangle "Device Repository" as deviceRegistry
  rectangle "Device Catalog Client" as deviceCatalogClient
}

rectangle "Device Catalog Database" as deviceCatalogDb #FFE4E1

api --> deviceRegistry : запросы регистрации/удаления/активации/списка устройств для user_id
deviceRegistry --> deviceCatalogClient : чтение/запись данных устройств
deviceCatalogClient --> deviceCatalogDb : SQL доступ

@enduml

```



**Диаграмма кода (Code)**

Эта диаграмма классов представляет фасадную архитектуру для управления и запуска задач в приложении. Ядром является Command Processor, который выступает в роли фасада, скрывая сложную логику выполнения задач от внешних клиентов. 

Благодаря этой архитектуре можно добавлять новые функциональные возможности, не изменяя существующий код, что соответствует принципу открытости/закрытости (Open/Closed Principle). CommandProcessor и TaskHandlerFactory выступают в роли точек расширения, принимая новые типы ConcreteTaskInfo и ITaskHandlerPrototype соответственно. Эта структура обеспечивает гибкость и простоту обслуживания системы задач. 

```puml

@startuml
class TaskInfo {
    task_name: string
}

class ConcreteTaskInfo extends TaskInfo {
    -- Дополнительные поля для конкретной задачи --
    task_name: string  <<override>>
}

interface ITaskInvoker {
    + executeTask(TaskInfo task_info) {abstract}
}

class TaskInvoker implements ITaskInvoker {
    - taskHandlerFactory: ITaskHandlerFactory
    + executeTask(TaskInfo task_info)
}

interface ICommandProcessor {
    + executeConcreteCommand() {abstract}
}

class CommandProcessor implements ICommandProcessor {
    + executeConcreteCommand()
}

interface ITaskHandlerFactory {
    + createHandler(TaskInfo task_info) : ITaskHandlerPrototype {abstract}
}

class TaskHandlerFactory implements ITaskHandlerFactory {
    - prototypes: Map<string, ITaskHandlerPrototype>
    + createHandler(TaskInfo task_info) : ITaskHandlerPrototype
}

interface ITaskHandlerPrototype {
    + executeTask(TaskInfo task_info) {abstract}
    + clone() : ITaskHandlerPrototype {abstract}
}

class ConcreteTaskHandler implements ITaskHandlerPrototype {
    + executeTask(TaskInfo task_info)
    + clone() : ITaskHandlerPrototype
}

TaskInvoker -- ITaskHandlerFactory : uses >
CommandProcessor --  ConcreteTaskInfo : uses >
CommandProcessor -- ITaskInvoker : uses >
TaskHandlerFactory -- ITaskHandlerPrototype : uses >
ConcreteTaskHandler -- ConcreteTaskInfo : uses >

@enduml

```



# Задание 3. Разработка ER-диаграммы

Добавьте сюда ER-диаграмму. Она должна отражать ключевые сущности системы, их атрибуты и тип связей между ними.

```puml

@startuml
title Общая ER-диаграмма

entity "User" as User {
  * user_id : UUID <<PK>>
  --
  username : varchar
  email : varchar
  password_hash : varchar
  created_at : timestamp
  updated_at : timestamp
}

entity "DeviceGroup" as DeviceGroup {
  * group_id : UUID <<PK>>
  --
  name : varchar
  description : varchar
  user_id : UUID <<FK>>
  created_at : timestamp
  updated_at : timestamp
}

entity "Device" as Device {
  * device_id : UUID <<PK>>
  --
  serial_number : varchar
  name : varchar
  type : varchar
  status : varchar
  user_id : UUID <<FK>>
  group_id : UUID <<FK>>
  description : varchar
  settings : json
  created_at : timestamp
  updated_at : timestamp
}

entity "TemperatureRecord" as TempRecord {
  * record_id : UUID <<PK>>
  --
  device_id : UUID <<FK>>
  temperature : float
  recorded_at : timestamp
}

entity "VideoRecord" as VideoRecord {
  * video_id : UUID <<PK>>
  --
  device_id : UUID <<FK>>
  file_path : varchar
  start_time : timestamp
  end_time : timestamp
}

entity "MotionEvent" as MotionEvent {
  * event_id : UUID <<PK>>
  --
  video_id : UUID <<FK>>
  detected_at : timestamp
  event_type : varchar
  description : varchar
}

' Связи

User ||--o{ DeviceGroup : владеет >
User ||--o{ Device : владеет >
DeviceGroup ||--o{ Device : содержит >

Device ||--o{ TempRecord : генерирует >
Device ||--o{ VideoRecord : генерирует >
VideoRecord ||--o{ MotionEvent : содержит >

@enduml

```


# Задание 4. Создание и документирование API

### 1. Тип API

В данной системе я буду использовать REST API для всех взаимодействий, так как требуется быстрое получение информации и управление устройствами. В данном варианте системы пока не рассматриваю, как конкретно будут отправляться Alarms пользователю и как они будут обрабатываться, т.к. тут еще нужно подумать и спроектировать это отдельно. Пока просто предусмотрю, что события можно запросить у конкретного сервиса. 


### 2. Документация API

Здесь приложите ссылки на документацию API для микросервисов, которые вы спроектировали в первой части проектной работы. Для документирования используйте Swagger/OpenAPI или AsyncAPI.

```puml

openapi: 3.0.3
info:
  title: API Application API
  version: 1.0.0
paths:
  /users:
    get:
      summary: Получить список пользователей
      responses:
        '200':
          description: Список пользователей
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    post:
      summary: Создать нового пользователя
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
      responses:
        '201':
          description: Пользователь создан
  /users/{userId}:
    get:
      summary: Получить пользователя по ID
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Данные пользователя
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
    put:
      summary: Обновить данные пользователя
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserUpdate'
      responses:
        '200':
          description: Пользователь обновлён
    delete:
      summary: Удалить пользователя
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Пользователь удалён
  /devices/{userId}:
    get:
      summary: Получить список устройств
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Список устройств
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Device'
    post:
      summary: Зарегистрировать новое устройство
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DeviceCreate'
      responses:
        '201':
          description: Устройство зарегистрировано
  /devices/{userId}/{deviceId}:
    get:
      summary: Получить устройство по ID
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Информация об устройстве
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Device'
    put:
      summary: Обновить устройство
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DeviceUpdate'
      responses:
        '200':
          description: Устройство обновлено
    delete:
      summary: Удалить устройство
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Устройство удалено

components:
  schemas:
    User:
      type: object
      properties:
        user_id:
          type: string
          format: uuid
        username:
          type: string
        email:
          type: string
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
    UserCreate:
      type: object
      required:
        - username
        - email
        - password
      properties:
        username:
          type: string
        email:
          type: string
        password:
          type: string
    UserUpdate:
      type: object
      properties:
        username:
          type: string
        email:
          type: string
    Device:
      type: object
      properties:
        device_id:
          type: string
          format: uuid
        serial_number:
          type: string
        name:
          type: string
        type:
          type: string
        status:
          type: string
        user_id:
          type: string
          format: uuid
        group_id:
          type: string
          format: uuid
        description:
          type: string
        settings:
          type: object
          description: "Настройки устройства в формате JSON"
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
    DeviceCreate:
      type: object
      required:
        - serial_number
        - name
        - type
        - _user_id
      properties:
        serial_number:
          type: string
        name:
          type: string
        type:
          type: string
        user_id:
          type: string
          format: uuid
        group_id:
          type: string
          format: uuid
        description:
          type: string
        settings:
          type: object
    DeviceUpdate:
      type: object
      properties:
        name:
          type: string
        status:
          type: string
        group_id:
          type: string
          format: uuid
        description:
          type: string
        settings:
          type: object


```



```puml

openapi: 3.0.3
info:
  title: Heating Control Service API
  version: 1.0.0
paths:
  /commands:
    post:
      summary: Отправить команду на отопительное устройство
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/HeatingCommand'
      responses:
        '200':
          description: Команда принята
  /status/{deviceId}:
    get:
      summary: Получить состояние отопительного устройства
      parameters:
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Текущее состояние устройства
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HeatingStatus'
components:
  schemas:
    HeatingCommand:
      type: object
      required:
        - device_id
        - command
      properties:
        device_id:
          type: string
          format: uuid
        command:
          type: string
          description: 'turn_on, turn_off, set_temperature'
        parameters:
          type: object
          description: 'Параметры команды'
    HeatingStatus:
      type: object
      properties:
        device_id:
          type: string
          format: uuid
        is_on:
          type: boolean
        current_temperature:
          type: number
          format: float
        target_temperature:
          type: number
          format: float
        updated_at:
          type: string
          format: date-time

```




```puml

openapi: 3.0.3
info:
  title: Temperature Monitoring Service API
  version: 1.0.0
paths:
  /records/{deviceId}:
    get:
      summary: Получить записи температуры по устройству
      parameters:
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: from
          in: query
          required: false
          schema:
            type: string
            format: date-time
        - name: to
          in: query
          required: false
          schema:
            type: string
            format: date-time
      responses:
        '200':
          description: Список записей температуры
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/TemperatureRecord'
  /monitoring:
    post:
      summary: Настроить мониторинг температуры
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MonitoringSettings'
      responses:
        '200':
          description: Настройки применены
components:
  schemas:
    TemperatureRecord:
      type: object
      properties:
        record_id:
          type: string
          format: uuid
        device_id:
          type: string
          format: uuid
        temperature:
          type: number
          format: float
        recorded_at:
          type: string
          format: date-time
    MonitoringSettings:
      type: object
      properties:
        device_id:
          type: string
          format: uuid
        interval_seconds:
          type: integer
          description: Интервал сбора данных
        threshold_min:
          type: number
          format: float
          description: Минимальный порог температуры
        threshold_max:
          type: number
          format: float
          description: Максимальный порог температуры

```




```puml

openapi: 3.0.3
info:
  title: Light Control Service API
  version: 1.0.0
paths:
  /commands:
    post:
      summary: Отправить команду управления освещением
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LightCommand'
      responses:
        '200':
          description: Команда принята
  /status/{deviceId}:
    get:
      summary: Получить состояние устройства освещения
      parameters:
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Состояние устройства
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LightStatus'
components:
  schemas:
    LightCommand:
      type: object
      required:
        - device_id
        - command
      properties:
        device_id:
          type: string
          format: uuid
        command:
          type: string
          description: 'turn_on, turn_off, set_brightness, set_color'
        parameters:
          type: object
          description: 'Параметры команды'
    LightStatus:
      type: object
      properties:
        device_id:
          type: string
          format: uuid
        is_on:
          type: boolean
        brightness:
          type: integer
          description: 'Уровень яркости (0-100)'
        color:
          type: string
          description: 'Цвет освещения'
        updated_at:
          type: string
          format: date-time

```




```puml

openapi: 3.0.3
info:
  title: Gate Control Service API
  version: 1.0.0
paths:
  /commands:
    post:
      summary: Отправить команду управления воротами
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/GateCommand'
      responses:
        '200':
          description: Команда принята
  /status/{deviceId}:
    get:
      summary: Получить состояние ворот
      parameters:
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Состояние ворот
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GateStatus'
components:
  schemas:
    GateCommand:
      type: object
      required:
        - device_id
        - command
      properties:
        device_id:
          type: string
          format: uuid
        command:
          type: string
          description: 'open, close, stop'
        parameters:
          type: object
          description: 'Параметры команды'
    GateStatus:
      type: object
      properties:
        device_id:
          type: string
          format: uuid
        is_open:
          type: boolean
        is_moving:
          type: boolean
        updated_at:
          type: string
          format: date-time

```




```puml

openapi: 3.0.3
info:
  title: Gate Monitoring Service API
  version: 1.0.0
paths:
  /status/{deviceId}:
    get:
      summary: Получить статус ворот в реальном времени
      parameters:
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Статус ворот
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GateStatus'
  /alerts/{deviceId}:
    get:
      summary: Получить события и уведомления по воротам
      parameters:
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Список событий
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/GateAlert'
components:
  schemas:
    GateStatus:
      type: object
      properties:
        device_id:
          type: string
          format: uuid
        is_open:
          type: boolean
        is_moving:
          type: boolean
        updated_at:
          type: string
          format: date-time
    GateAlert:
      type: object
      properties:
        alert_id:
          type: string
          format: uuid
        device_id:
          type: string
          format: uuid
        alert_type:
          type: string
        message:
          type: string
        timestamp:
          type: string
          format: date-time

```




```puml

openapi: 3.0.3
info:
  title: Video & Camera Service API
  version: 1.0.0
paths:
  /videos/{deviceId}:
    get:
      summary: Получить список видеофайлов с камеры
      parameters:
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Список видео
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/VideoRecord'
  /videos/file/{videoId}:
    get:
      summary: Получить видеофайл по ID
      parameters:
        - name: videoId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Видео файл
          content:
            video/mp4:
              schema:
                type: string
                format: binary
  /stream-url/{deviceId}:
    get:
      summary: Получить URL для потокового видео с камеры
      parameters:
        - name: deviceId
          in: path
          required: true
          description: Идентификатор устройства камеры
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: URL потокового видео
          content:
            application/json:
              schema:
                type: object
                properties:
                  stream_url:
                    type: string
                    format: uri
                    example: "rtsp://camera.example.com/stream/12345"
        '404':
          description: Камера не найдена 
  /motion-events:
    post:
      summary: Зарегистрировать событие детекции движения
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MotionEvent'
      responses:
        '201':
          description: Событие зарегистрировано
  /motion-events/{deviceId}:
    get:
      summary: Получить события детекции движения по устройству
      parameters:
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Список событий
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/MotionEvent'
components:
  schemas:
    VideoRecord:
      type: object
      properties:
        video_id:
          type: string
          format: uuid
        device_id:
          type: string
          format: uuid
        file_path:
          type: string
        start_time:
          type: string
          format: date-time
        end_time:
          type: string
          format: date-time
    MotionEvent:
      type: object
      required:
        - video_id
        - detected_at
      properties:
        event_id:
          type: string
          format: uuid
        video_id:
          type: string
          format: uuid
        detected_at:
          type: string
          format: date-time
        event_type:
          type: string
        description:
          type: string

```




```puml

openapi: 3.0.3
info:
  title: Common Device Service API
  version: 1.0.0
paths:
  /register:
    post:
      summary: Регистрация нового устройства
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DeviceRegistration'
      responses:
        '201':
          description: Устройство зарегистрировано
  /activate/{deviceId}:
    post:
      summary: Активация устройства
      parameters:
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Устройство активировано
  /deactivate/{deviceId}:
    post:
      summary: Деактивация устройства
      parameters:
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Устройство деактивировано
  /list/{userId}:
    get:
      summary: Получить список устройств пользователя
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Список устройств
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/DeviceSummary'
components:
  schemas:
    DeviceRegistration:
      type: object
      required:
        - serial_number
        - name
        - type
        - user_id
      properties:
        serial_number:
          type: string
        name:
          type: string
        type:
          type: string
        user_id:
          type: string
          format: uuid
        group_id:
          type: string
          format: uuid
        description:
          type: string
        settings:
          type: object
    DeviceSummary:
      type: object
      properties:
        device_id:
          type: string
          format: uuid
        name:
          type: string
        type:
          type: string
        status:
          type: string

```

# Задание 5. Работа с docker и docker-compose

Перейдите в apps.

Там находится приложение-монолит для работы с датчиками температуры. В README.md описано как запустить решение.

Вам нужно:

1) сделать простое приложение temperature-api на любом удобном для вас языке программирования, которое при запросе /temperature?location= будет отдавать рандомное значение температуры.

Locations - название комнаты, sensorId - идентификатор названия комнаты

```
	// If no location is provided, use a default based on sensor ID
	if location == "" {
		switch sensorID {
		case "1":
			location = "Living Room"
		case "2":
			location = "Bedroom"
		case "3":
			location = "Kitchen"
		default:
			location = "Unknown"
		}
	}

	// If no sensor ID is provided, generate one based on location
	if sensorID == "" {
		switch location {
		case "Living Room":
			sensorID = "1"
		case "Bedroom":
			sensorID = "2"
		case "Kitchen":
			sensorID = "3"
		default:
			sensorID = "0"
		}
	}
```

2) Приложение следует упаковать в Docker и добавить в docker-compose. Порт по умолчанию должен быть 8081

3) Кроме того для smart_home приложения требуется база данных - добавьте в docker-compose файл настройки для запуска postgres с указанием скрипта инициализации ./smart_home/init.sql

Для проверки можно использовать Postman коллекцию smarthome-api.postman_collection.json и вызвать:

- Create Sensor
- Get All Sensors

Должно при каждом вызове отображаться разное значение температуры

Ревьюер будет проверять точно так же.


