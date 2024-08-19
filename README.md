# Vision-Based Mobility and Navigation Aid for the Visually Challenged People
*[Paper Link](https://pubs.aip.org/aip/acp/article-abstract/2851/1/030007/2921920/Vision-based-mobility-and-navigation-aid-for-the?redirectedFrom=fulltext)*

The project aims to assist visually impaired individuals with navigation by providing real-time obstacle avoidance and route guidance. The system takes a voice command to set the user's desired destination, then identifies and guides the user along a complete route, notifying them when a turn is needed. Simultaneously, it executes an obstacle avoidance model that alerts the user when an obstacle is nearby. The system is designed to operate in real-time, with controlled delays between voice commands to prevent overwhelming the user, resulting in an improved navigation and obstacle avoidance experience.

<hr>

## Introduction:

- An estimated 285 million Visually Impaired people in the world
- The risk of mortality associated with Visual Impairment in a study was around 25% casualties
- Secure and Independent Mobility is a challenge for the Visually Impaired
- Mobility and Navigation Difficulties can be solved with Electronic Travel Assistance

## Research Gap:

- Lack of Useful Functions
- Inaccurate Distance Estimation
- Bulky and Heavy-Weight
- Ergonomic and Aesthetic
- Steep Learning Curve
- Expensive

## Proposed Solution:

- Modular Assistive System
- Consists of two Independent Modules:
  - Object Detection Module
  - Voice Interactive Orientation and Navigation Module
- Object Detection Module for Detection and Avoidance
- Navigation Module for Navigation and Path Planning
- Simplified Audio Feedback

## Novelty:

- Obstacle Detection, Depth Estimation and Route Estimation
- Rerouting Capability
- Convenient Carry and Lightweight
- No Geographical Bounds
- Low Power Consumption
- Inexpensive

## Methodolgy:
### Architecture of the Proposed System:

<img src="figures\main_block_diagram.png" alt="Architecture of the Proposed System" width="500"/>

<br>

### Object Detection Module:

<img src="figures\object_detection.png" alt="Architecture of the Object Detection Module" width="500"/>

<br>

### HSV Thresholding:

<img src="figures\HSV_threshold.png" alt="HSV Thresholding and Object Detection" width="500"/>

<br>

### Navigation Module:

<img src="figures\navigation.png" alt="Architecture of the Navigation Module" width="500"/>

<br>

## Results:

**Study Design**
- Experiments: 10
- Environment: Footpath (4m-5m Wide)
- Condition: Medium Crowded
- Subjects: Individuals with camera strapped on their chest

**Combined Precision and Recall for the Detected Obstacles:**
- Recall: 91.7%
- Precision: 81.5%

## Advantages & Limitations:

**Advantages:**
- Simplified Audio Feedback
- Real-Time Implementation
- Blend of Obstacle and Navigation
- Low Power Embedded System
- Wearable System
- High Precision
- Cost Effective

**Limitations:**
- Required Uniform Illumination
- Low GPS Accuracy

## Conclusion:

- Implemented a new method for the Visual-Based Navigation System for the Visually Impaired.
- Reduced Information Load for Mobility and Navigation Assistance
- Simplified representation of the Surrounding Environment
- Accuracy:
  - Object Detection: 91.7%
  - Orientation and Navigation: 77%

<br>
<hr>
